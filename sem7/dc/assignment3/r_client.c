#include<sys/types.h>
#include<sys/time.h>
#include<time.h>
#include<errno.h>
#include<stdio.h>
#include<signal.h>
#include<stdlib.h>
#include<unistd.h>
#include<rpc/rpc.h>
#include<netinet/in.h>
#include"square.h"

int main(int argc,char **argv){
CLIENT *cl;
square_in in;
square_out *outp;
if(argc!=3)exit(0);
cl=clnt_create(argv[1],SQUARE_PROG,SQUARE_VER,"tcp");
in.arg1=atol(argv[2]);
if((outp=squareproc_1(&in,cl))==NULL)exit(0);
printf("result: %ld\n",outp->res1);
exit(0);
}
