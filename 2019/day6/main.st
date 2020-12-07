a := Day6 new.
f := '/home/jaume/Sync/proj/aoc/day6/input.txt' asFileReference.
stream := f readStream.
text := stream upToEnd.
{a count: text.
a countTransfers: text}
