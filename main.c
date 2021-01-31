#include <stdio.h>
#include <errno.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <unistd.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <string.h>

#include "messages.h"
#define CBSIZE 2048

const char *blocked[] = {
    "MIF",
    "attack",
    "unexpectedEOF",
    "jan3",
    "c-69-255-237-187.hsd1.md.comcast.net"
};
const char *blockmsg = "Error 404: no";
const char *username = "guest_03384";
const char *channel = "#chaos";
const char *topic = "rule one: you are now a duck. ・゜゜・。。・゜゜\\_o< QUACK!";
const char *owner = "rndusr";

/* 
 * should contain
 * const char *password = "your face";
 * or the like.
*/
#include "secrets.h"

typedef struct cbuf {
    char buf[CBSIZE];
    int fd;
    unsigned int rpos, wpos;
} cbuf_t;


int read_line(cbuf_t *cbuf, char *dst, unsigned int size)
{
    unsigned int i = 0;
    ssize_t n;
    while (i < size) {
        if (cbuf->rpos == cbuf->wpos) {
            size_t wpos = cbuf->wpos % CBSIZE;
            //if ((n = read(cbuf->fd, cbuf->buf + wpos, (CBSIZE - wpos))) < 0) {
            if((n = recv(cbuf->fd, cbuf->buf + wpos, (CBSIZE - wpos), 0)) < 0) {
                if (errno == EINTR)
                    continue;
                return -1;
            } else if (n == 0)
                return 0;
            cbuf->wpos += n;
        }
        dst[i++] = cbuf->buf[cbuf->rpos++ % CBSIZE];
        if (dst[i - 1] == '\n')
            break;
    }
    if(i == size) {
         fprintf(stderr, "line too large: %d %d\n", i, size);
         return -1;
    }

    dst[i] = 0;
    return i;
}

int main()
{
    cbuf_t *cbuf;
    char buf[4096];
    struct sockaddr_in saddr;
    struct hostent *h;
    const char host[] = "localhost";
    const int port = 6667;
    char *ip;

    if(!(h = gethostbyname(host))) {
        perror("gethostbyname");
        return 2;
    }
    ip = inet_ntoa(*(struct in_addr*)h->h_addr);

    cbuf = calloc(1, sizeof(*cbuf));

    fprintf(stdout, "Connecting to ip: %s\n", ip);
    if((cbuf->fd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("socket");
        return 1;
    }
    memset(&saddr, 0, sizeof(saddr));
    saddr.sin_family = AF_INET;
    saddr.sin_port = htons(port);
    inet_aton(ip, &saddr.sin_addr);
    if(connect(cbuf->fd, (struct sockaddr*)&saddr, sizeof(saddr)) < 0) {
        perror("connect");
        return 1;
    }

    snprintf(buf, sizeof(buf), "USER %s 0 * :test\r\n", username, host);
    write(cbuf->fd, buf, strlen(buf));
    snprintf(buf, sizeof(buf), "NICK %s\r\n", username, host);
    write(cbuf->fd, buf, strlen(buf));
    while(read_line(cbuf, buf, sizeof(buf)) > 0) {
	if(strstr(buf, "001") != NULL) {
		printf("%s", buf);
		break;
	}
        printf("%s", buf);
    }
    snprintf(buf, sizeof(buf), "JOIN %s\r\n", channel, host);
    write(cbuf->fd, buf, strlen(buf));
    snprintf(buf, sizeof(buf), "PRIVMSG NickServ :identify %s\r\n", password, host);
    write(cbuf->fd, buf, strlen(buf));
    while(read_line(cbuf, buf, sizeof(buf)) > 0) {
	if(strstr(buf, "hello loser") != NULL) {
    		snprintf(buf, sizeof(buf), "PRIVMSG %s :you're a loser\r\n", channel, host);
    		write(cbuf->fd, buf, strlen(buf));
    		snprintf(buf, sizeof(buf), "NOTICE %s :you're a loser\r\n", channel, host);
    		write(cbuf->fd, buf, strlen(buf));
    		snprintf(buf, sizeof(buf), "PRIVMSG %s :someone called me loser :(\r\n", owner, host);
    		write(cbuf->fd, buf, strlen(buf));
	}
	if(strstr(buf, "PING") != NULL ) {
    		snprintf(buf, sizeof(buf), "PONG :club.tilde.chat\r\n", host);
    		write(cbuf->fd, buf, strlen(buf));
	}
	if(strstr(buf, "KICK") != NULL ) {
    		snprintf(buf, sizeof(buf), "JOIN %s\r\n", channel, host);
    		write(cbuf->fd, buf, strlen(buf));
	}
	if(strstr(buf, "JOIN") != NULL) {
		for(int i = 0; i <= sizeof(blocked)/sizeof(blocked[0]); i++) {
			if(strstr(buf, blocked[i]) != NULL) {
	    			snprintf(buf, sizeof(buf), "KICK %s %s :%s\r\n", channel, blocked[i], blockmsg, host);
	    			write(cbuf->fd, buf, strlen(buf));
			}
		}
	}
	if(strstr(buf, "ban") != NULL) {
		snprintf(buf, sizeof(buf), "PRIVMSG ChanServ :unban %s %s\r\n", channel, username, host);
    		write(cbuf->fd, buf, strlen(buf));
		snprintf(buf, sizeof(buf), "PRIVMSG ChanServ :owner %s %s\r\n", channel, username, host);
    		write(cbuf->fd, buf, strlen(buf));
		snprintf(buf, sizeof(buf), "PRIVMSG ChanServ :invite %s %s\r\n", channel, username, host);
    		write(cbuf->fd, buf, strlen(buf));
		snprintf(buf, sizeof(buf), "JOIN %s\r\n", channel, username, host);
    		write(cbuf->fd, buf, strlen(buf));
	}
	if(strstr(buf, "TOPIC") != NULL) {
		sleep(1);
    		snprintf(buf, sizeof(buf), "TOPIC %s :%s\r\n", channel, topic);
    		write(cbuf->fd, buf, strlen(buf));
	}
        printf("%s", buf);
    }
    close(cbuf->fd);
    free(cbuf);
    return 0;
}
