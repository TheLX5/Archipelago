from bisect import bisect_right
from dataclasses import dataclass
import enum
import logging
from typing import TYPE_CHECKING, Generic, NamedTuple, Sequence, TypeVar

if TYPE_CHECKING:
    from SNIClient import SNIContext

SNES_READ_CHUNK_SIZE = 2048


class Read(NamedTuple):
    """ snes memory read - address and size in bytes """
    address: int
    size: int


@dataclass(frozen=True)
class _MemRead:
    location: Read
    data: bytes


_T_Enum = TypeVar("_T_Enum", bound=enum.Enum)


class SnesData(Generic[_T_Enum]):
    _ranges: Sequence[_MemRead]
    """ sorted by address """

    def __init__(self, ranges: Sequence[tuple[Read, bytes]]) -> None:
        self._ranges = []
        for r, d in ranges:
            self._ranges.append(_MemRead(r, d))

    def get(self, read: _T_Enum) -> bytes:
        assert isinstance(read.value, Read), read.value
        address = read.value.address
        index = bisect_right(self._ranges, address, key=lambda r: r.location.address) - 1
        assert index >= 0, (self._ranges, read.value)
        mem_read = self._ranges[index]
        sub_index = address - mem_read.location.address
        return mem_read.data[sub_index:sub_index + read.value.size]


class SnesReader(Generic[_T_Enum]):
    """
    how to use:
    ```
    from enum import Enum
    from worlds.AutoSNIClient import Read, SNIClient, SnesReader
    class MyGameMemory(Enum):
        game_mode = Read(WRAM_START + 0x0998, 1)
        send_queue = Read(SEND_QUEUE_START, 8 * 127)
        ...
    snes_reader = SnesReader(MyGameMemory)
    snes_data = await snes_reader.read(ctx)
    if snes_data is None:
        snes_logger.info("error reading from snes")
        return
    game_mode = snes_data.get(MyGameMemory.game_mode)
    ```
    """
    _ranges: Sequence[Read]
    """ sorted by address """

    def __init__(self, reads: type[_T_Enum]) -> None:
        self._ranges = self._make_ranges(reads)

    @staticmethod
    def _make_ranges(reads: type[enum.Enum]) -> Sequence[Read]:

        unprocessed_reads: list[Read] = []
        for e in reads:
            assert isinstance(e.value, Read), (reads.__name__, e, e.value)
            unprocessed_reads.append(e.value)
        unprocessed_reads.sort()

        ranges: list[Read] = []
        for read in unprocessed_reads:
            #                                      v  end of the previous range
            if len(ranges) == 0 or read.address - (ranges[-1].address + ranges[-1].size) > 255:
                ranges.append(read)
            else:  # combine with previous range
                chunk_address = ranges[-1].address
                assert read.address >= chunk_address, "sort() didn't work? or something"
                original_chunk_size = ranges[-1].size
                new_size = max((read.address + read.size) - chunk_address,
                               original_chunk_size)
                ranges[-1] = Read(chunk_address, new_size)
        logging.debug(f"{len(ranges)=} {max(r.size for r in ranges)=}")
        return ranges

    async def read(self, ctx: "SNIContext") -> SnesData[_T_Enum] | None:
        """
        returns `None` if reading fails,
        otherwise returns the data for the registered `Enum`
        """
        from SNIClient import snes_read

        reads: list[tuple[Read, bytes]] = []
        for r in self._ranges:
            if r.size < SNES_READ_CHUNK_SIZE:  # most common
                response = await snes_read(ctx, r.address, r.size)
                if response is None:
                    return None
                reads.append((r, response))
            else:  # big read
                # Problems were reported with big reads,
                # so we chunk it into smaller pieces.
                read_so_far = 0
                collection: list[bytes] = []
                while read_so_far < r.size:
                    remaining_size = r.size - read_so_far
                    chunk_size = min(SNES_READ_CHUNK_SIZE, remaining_size)
                    response = await snes_read(ctx, r.address + read_so_far, chunk_size)
                    if response is None:
                        return None
                    collection.append(response)
                    read_so_far += chunk_size
                reads.append((r, b"".join(collection)))
        return SnesData(reads)
