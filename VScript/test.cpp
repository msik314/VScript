#include <cstdio>

int main(int argc, char** argv)
{
if(argc > 1)
goto Block1;
else
goto Block3;
Block1:
printf("Extra arguments given\n");
goto Block2;
Block3:
printf("Hello World!\n");
goto Block2;
Block2:
printf("Joined back up!\n");
return 0;
}
