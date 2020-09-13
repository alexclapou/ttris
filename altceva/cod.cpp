#include <iostream>
#include <stdio.h>
#include <termios.h>
#include <unistd.h>
#include <fcntl.h>
#include <ncurses.h>
#include <ctime>
#include <stdlib.h>
using namespace std;
int kbhit(void)
{
  struct termios oldt, newt;
  int ch;
  int oldf;

  tcgetattr(STDIN_FILENO, &oldt);
  newt = oldt;
  newt.c_lflag &= ~(ICANON | ECHO);
  tcsetattr(STDIN_FILENO, TCSANOW, &newt);
  oldf = fcntl(STDIN_FILENO, F_GETFL, 0);
  fcntl(STDIN_FILENO, F_SETFL, oldf | O_NONBLOCK);

  ch = getchar();

  tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
  fcntl(STDIN_FILENO, F_SETFL, oldf);

  if(ch != EOF)
  {
    ungetc(ch, stdin);
    return 1;
  }

  return 0;
}

const int LMAX=60,HMAX=10;
bool GameOver;
struct sprite
{
    int x;
    int y;
    char skin;
}player;
enum directii
{
    STOP,
    LEFT,
    RIGHT,
    UP,
    DOWN,
}DirPlayer;
void Setup ()
{
    srand((unsigned)time(0));
    player.x= rand()%(LMAX-1);
    player.y= rand()%(HMAX-1);
    player.skin='A';
    GameOver=false;
    DirPlayer=STOP;
}
void Draw (sprite player)
{
    for (int i=1; i<=LMAX; i++) cout<<'#';
    cout<<endl;
    for (int i=1; i<=HMAX; i++)
    {
        cout<<'#';
        for (int j=2; j<LMAX; j++)
        {
            if (j==player.x && i==player.y) cout<<player.skin;
            else cout<<" ";
        }
        cout<<'#'<<endl;
    }
    for (int i=1; i<=LMAX; i++) cout<<'#';
}
void Input ()
{
    if (kbhit())
    {
        switch (getch())
        {
            case 'a': DirPlayer=LEFT;break;
            case 'd': DirPlayer=RIGHT;break;
            case 'w': DirPlayer=UP;break;
            case 's': DirPlayer=DOWN;break;
        }
    }
}
void Logic ()
{
    switch (DirPlayer)
    {
        case LEFT: player.x--;
            break;
        case RIGHT: player.x++;
            break;
        case UP: player.y++;
            break;
        case DOWN: player.y--;
            break;
    }
}
int main()
{
    Setup();
    Draw(player);
    Input();
    Logic();
    return 0;
}
