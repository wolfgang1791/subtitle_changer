from datetime import timedelta, datetime

def parse_timecode(tc: str) -> datetime:
    """Convert an SRT timecode (HH:MM:SS,mmm) into a datetime object."""
    return datetime.strptime(tc.strip(), "%H:%M:%S,%f")

def format_timecode(dt: datetime) -> str:
    """Convert datetime back into SRT timecode (HH:MM:SS,mmm)."""
    return dt.strftime("%H:%M:%S,%f")[:-3]  # trim extra microseconds

def shift_timecode(tc: str, seconds: float, mode: str) -> str:
    """Shift the timecode forward ('go') or backward ('gos') by given seconds."""
    dt = parse_timecode(tc)
    delta = timedelta(seconds=seconds)
    dt = dt + delta if mode == "go" else dt - delta
    return format_timecode(dt)

def adjust_subtitles(filename: str, seconds: float, mode: str = "go"):
    """Adjust subtitle timestamps from an SRT/TXT file."""
    with open(filename + ".txt", encoding="utf-8") as f, \
         open(filename + "_new.txt", "w", encoding="utf-8") as out:

        for line in f:
            if "-->" in line:
                start, end = line.split("-->")
                start = shift_timecode(start.strip(), seconds, mode)
                end = shift_timecode(end.strip(), seconds, mode)
                newline = f"{start} --> {end}\n"
                out.write(newline)
                print(newline, end="")
            else:
                out.write(line)

# Example usage:
adjust_subtitles("thecircle", seconds=5, mode="gos")  
# mode="go" -> shift forward, mode="gos" -> shift backward
