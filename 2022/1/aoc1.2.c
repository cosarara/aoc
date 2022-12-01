#include <u.h>
#include <libc.h>
#include <bio.h>

void
main()
{
	Biobuf* bf;
	Biobuf bstdin;
	if (Binit(&bstdin, 0, OREAD) == Beof) {
		perror("opening stdin");
		exits("opening stdin");
	}
	bf = &bstdin;
	char *line;
	int curr = 0;

	while (1) {
		line = Brdstr(bf, '\n', 1);
		if (line == nil || line[0] == 0) {
			print("%d\n", curr);
			curr = 0;
			if (line == nil) break;
			continue;
		}
		int val = atoi(line);
		curr += val;
	}
	exits(0);
}