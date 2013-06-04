#include <unistd.h>
#include <iostream>
#include <cstring>
#include <netdb.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sstream>
#include <stdio.h>

ssize_t http_request(int sfd, char *poststr)
{
	char sendl[4097], recvl[4097];
	ssize_t n;
	int len = strlen(poststr);
	std::ostringstream ss;
	ss << len;
	snprintf(sendl, 300,
		 "POST /~qijia.jin/reaction/process.py HTTP/1.0\r\n\r"
		 "Host: 149.89.150.100\r\n"
		 "Content-type: application/x-www-form-urlencoded\r\n"
		 "Content-length: %d\r\n\r\n"
		 "%s", len, poststr);
	write(sfd, sendl, strlen(sendl));
	while ((n = read(sfd, recvl, 4097)) > 0) {
		recvl[n] = '\0';
	}
	return n;

}

int main(){
	int status;
	int socketfd;
	FILE *bfile;
	char id[100];
	std::string st;
	std::string st1;
	char* mrsrv;
	long int ps;
	std::cout << "Please enter the sentence you would like to submit to the story:" << std::endl;
	getline(std::cin,st);
	std::replace(st.begin(), st.end(), ' ', '+');
	const char *buff = st.c_str();
	const char *bbuff = st1.c_str();
	char *id0 = "id=";
	char *id1 = "append=";
	strcpy(id,id0);
	strcat(id,getlogin());
	strcat(id,"&");
	strcat(id,id1);
	strcat(id,buff);
	struct addrinfo host_info;
	struct addrinfo *host_info_list;
	memset(&host_info, 0, sizeof host_info);
	host_info.ai_family = AF_UNSPEC;
	host_info.ai_socktype = SOCK_STREAM;
	status = getaddrinfo("149.89.150.100", "80", &host_info, &host_info_list);
	socketfd = socket(AF_INET, SOCK_STREAM, host_info_list->ai_protocol);
	if (status != 0) {
		std::cout << "getaddrinfo() error: " << gai_strerror(status) << std::endl;
	}
	if (socketfd == -1) {
		std::cout << "Socket error: socket could not be created." << std::endl;
	}
	status = connect(socketfd, host_info_list->ai_addr, host_info_list->ai_addrlen);
	if (status == -1) {
		std::cout << "connect error" << std::endl;
	}
	http_request(socketfd,(char*)id);
	close(socketfd);
}
