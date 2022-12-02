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
	int points = 0;

	while (1) {
		line = Brdstr(bf, '\n', 1);
		if (line == nil) break;
		if (strlen(line) != 3) exits("bad line");
		char opponent = line[0];
		char ours = line[2];

		if (ours == 'X') points += 1;
		else if (ours == 'Y') points += 2;
		else points += 3;

		if (ours-'X' == opponent-'A'+1 || ours=='X' && opponent=='C')
		{
			// victory
			points += 6;
		} else if (ours-'X' == opponent-'A') {
			// tie
			points += 3;
		}
	}
	print("points %d\n", points);
	exits(0);
}
