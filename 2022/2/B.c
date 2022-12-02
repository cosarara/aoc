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
		char target = line[2];
		char ours = 'A';

		if (target == 'X') { // lose
			if (opponent == 'A') ours = 'C';
			else ours = opponent-1;
		} else if (target == 'Y') { // tie
			ours = opponent;
		} else { // win
			if (opponent == 'C') ours = 'A';
			else ours = opponent+1;
		}

		if (ours == 'A') points += 1;
		else if (ours == 'B') points += 2;
		else points += 3;

		if (ours == opponent+1 || ours=='A' && opponent=='C')
		{
			// victory
			points += 6;
		} else if (ours == opponent) {
			// tie
			points += 3;
		}
	}
	print("points %d\n", points);
	exits(0);
}
