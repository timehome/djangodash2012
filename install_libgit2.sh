cd /tmp && wget https://github.com/libgit2/libgit2/zipball/development && mv development libgit2.zip && unzip libgit2.zip
cd /tmp/libgit2* && cmake .. && cmake --build . && sudo cmake --build . --target install
