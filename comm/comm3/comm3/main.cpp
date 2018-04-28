//
//  main.cpp
//  comm3
//
//  Created by Adam on 4/20/18.
//  Copyright © 2018 Adam. All rights reserved.
//

#include <iostream>
#include <string>
#include <termios.h>
#include <fcntl.h>
#include <unistd.h>

using namespace std;

int main(int argc, const char * argv[])
{
    if (argc < 2 || argc > 3)
    {
        cerr << "usage: " << argv[0] << " device [bauds]" << endl;
        return 1;
    }
    
    string device = argv[1];
    unsigned long bauds = 115200;
    if (argc == 3)
    {
        char* result;
        bauds = strtoul(argv[2], &result, 10);
        if (*result != '\0')
        {
            cerr << "usage: " << argv[0] << " device [bauds]" << endl;
            return 1;
        }
    }
    
    int fd = open(argv[1], O_RDWR | O_NDELAY | O_NOCTTY);
    if (fd == -1)
    {
        perror((string("can't open ") + argv[1]).c_str());
        exit(errno);
    }
    
    struct termios config;
    if (tcgetattr(fd, &config) < 0)
    {
        perror("can't get serial attributes");
        exit(errno);
    }
    
    if (cfsetispeed(&config, bauds) < 0 || cfsetospeed(&config, bauds) < 0)
    {
        perror("can't set baud rate");
        exit(errno);
    }
    
    config.c_iflag &= ~(IGNBRK | BRKINT | ICRNL | INLCR | PARMRK | INPCK | ISTRIP | IXON);
    config.c_oflag = 0;
    config.c_lflag &= ~(ECHO | ECHONL | ICANON | IEXTEN | ISIG);
    config.c_cflag &= ~(CSIZE | PARENB);
    config.c_cflag |= CS8;
    config.c_cc[VMIN]  = 1;
    config.c_cc[VTIME] = 0;
    
    if (tcsetattr(fd, TCSAFLUSH, &config) < 0)
    {
        perror("can't set serial attributes");
        exit(errno);
    }
    
    char buffer[80];
    while (true)
    {
        size_t n = read(fd, buffer, sizeof buffer);
        write(STDOUT_FILENO, buffer, n);
    }
    
    close(fd);
    return 0;
}
