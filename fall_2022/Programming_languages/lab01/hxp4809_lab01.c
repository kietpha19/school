/*
student name: Hoang Anh Kiet Pham
id: 1001904809
langauge version: gcc version 9.4.0, c-99 standard
operating system: Ubuntu (UTA virtual machine)
*/

#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <string.h>

/*
this function is to check if an entry name is a file or not
the logic was revised code from StackOverflow
the fuction take a char pointer as parameter, using struct stat to store the information of that entry
finally, return if that entry is a regular file or not
*/
int is_file(const char * file_name){
    struct stat st;
    stat(file_name,&st);
    return S_ISREG(st.st_mode);
}

/*
this function is to get the size of a file
the logic was revised code from StackOverflow
the function take a char pointer as parametre, using struct stat to store the information of the file
finnaly, return the astribute st_size of that file
*/
int get_size_of_file(char * file_name){
    struct stat st;
    stat(file_name, &st);
    return st.st_size;
}


/*
this function is to get the total size of current working direct story
the function take directory name as input, open the directory of check if success
then, the function change the current working directorty using chdir
after that, using struct dirent to get the name of every entry in current working directory
for each entry in the current directory:
    if the entry is file:
        add size of it to sum
    if the entry is directory (but but "." and ".."):
        recursively call the function again
        add the result to sum
        go back to parent directory
close the current directory
return sum
*/
long int get_total_size_of_dir(char * dir_name){
    DIR * current_dir = opendir(dir_name);
    if(current_dir == NULL){
        printf("could not open the directory %s\n", dir_name);
        return 0;
    }
    chdir(dir_name);
    long int sum = 0;
    struct dirent * entry;
    char current_dir_name[2] = ".";
    char parent_dir_name[3] = "..";
    while((entry = readdir(current_dir)) != NULL){
        if(is_file(entry->d_name) != 0){
            //printf("file: %s\n", entry->d_name); //for debugging pupose
            sum += get_size_of_file(entry->d_name);
        }
        else if (strcmp(entry->d_name, current_dir_name) != 0 && strcmp(entry->d_name, parent_dir_name) != 0)
        {
            //printf("dir: %s\n", entry->d_name); //for debugging pupose
            sum += get_total_size_of_dir(entry->d_name);
            chdir("..");
        }
        
    }
    closedir(current_dir);
    return sum;
}

int main(){
    long int total = 0; // variable to store the total size of
    total = get_total_size_of_dir(".");
    printf("%ld\n", total);

    return EXIT_SUCCESS;
}