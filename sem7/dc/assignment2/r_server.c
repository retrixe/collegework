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

square_out *squareproc_1_svc(square_in *inp,struct svc_req *rqstp){
static square_out out;
out.res1=inp->arg1*inp->arg1;
return &out;
}
