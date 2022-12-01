#include <u.h>
#include <libc.h>
#include <bio.h>

void
main()
{
	Biobuf *bf = Bopen("input1", OREAD);
	if (bf == nil) {
		perror("opening input1");
		exits("opening input1");
	}
	char *line;
	int max = 0;
	int curr = 0;

	while ((line = Brdstr(bf, '\n', 1)) != nil) {
		if (line[0] == 0) {
			if (curr > max) {
				max = curr;
			}
			curr = 0;
			continue;
		}
		int val = atoi(line);
		curr += val;
	}
	print("%d\n", max);
	exits(0);
}