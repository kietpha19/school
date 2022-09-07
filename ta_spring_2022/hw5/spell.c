#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "spell.h"

/*  Suggestions
- When you work with 2D arrays, be careful. Either manage the memory yourself, or
work with local 2D arrays. Note C99 allows parameters as array sizes as long as 
they are declared before the array in the parameter list. See: 
https://www.geeksforgeeks.org/pass-2d-array-parameter-c/

Worst case time complexity to compute the edit distance from T test words
 to D dictionary words where all words have length MAX_LEN:
Student answer:  Theta(............)


Worst case to do an unsuccessful binary search in a dictionary with D words, when 
all dictionary words and the searched word have length MAX_LEN 
Student answer:  Theta(............)
*/


/* You can write helper functions here */
int smallest(int x, int y, int z)
{
    int smallest;
    if((x <= y) && (x <= z))
        smallest = x;
    else if((y <= x) && (y <= z))
        smallest = y;
    else if((z <= x) && (z <= y))
        smallest = x;
    return smallest;
}


/*
Parameters:
first_string - pointer to the first string (displayed vertical in the table)
second_string - pointer to the second string (displayed horizontal in the table)
print_table - If 1, the table with the calculations for the edit distance will be printed.
              If 0 (or any value other than 1)it will not print the table
(See sample run)
Return:  the value of the edit distance (e.g. 3)
*/
int compare(const void *a, const void *b) 
{ 
    const char **str_a = (const char **)a;
    const char **str_b = (const char **)b;
    return strcmp(*str_a, *str_b);
} 
int edit_distance(char * first_string, char * second_string, int print_table)
{
    int first = strlen(first_string);
    int second = strlen(second_string);
    int value[first + 1][second + 1];
    for (int i = 0; i <= first; i++)
    {
        for(int j = 0; j <= second; j++ )
        {
            if(i == 0)
                value[i][j] = j;
            else if(j == 0)
                value[i][j] = i;
            else if(first_string[i - 1] == second_string[j - 1])
                value[i][j] = value[i - 1][j - 1];
            else
                value[i][j] = 1 + smallest(value[i][j - 1], value[i - 1][j], value[i - 1][j - 1]);
        }
    }
    if(print_table == 1)
    {
        for(int i = 0; i < first; i++)
        {
            for(int j = 0; j < second; j++)
            {
                printf("%d",value[i][j]);
                if(value[i][j] < 10)
                    printf(" /");
                else
                    printf("\n");
            }
            for(int j = 0; j < second; j++)
            {
                printf("---");
            }
            printf("\n");
        }
    }
	return value[first][second];  // replace this line with your code
}
	  

/*
Parameters:
testname - string containing the name of the file with the paragraph to spell check, includes .txt e.g. "text1.txt" 
dictname - name of file with dictionary words. Includes .txt, e.g. "dsmall.txt"
printOn - If 1 it will print EXTRA debugging/tracing information (in addition to what it prints when 0):
			 dictionary as read from the file	
			 dictionary AFTER sorting in lexicographical order
			 for every word searched in the dictionary using BINARY SEARCH shows all the "probe" words and their indices indices
			 See sample run.
	      If 0 (or anything other than 1) does not print the above information, but still prints the number of probes.
		     See sample run.
*/

int  MAX_LEN=100;
void spell_check(char * testname, char * dictname, int printOn)
{
	FILE * file1 = fopen(testname,"r");
    FILE * file2 = fopen(dictname,"r");
    int size,temp, length, count = 1, distance;
    char string[MAX_LEN];
    char * words[1000];
    int arr[100];
    char * dictionary[10000];
    arr[0] = 0;
    if(!file1)
    {
        printf("\nUnable to open files 1 for reading...");
        return;
    }
    if(!file2)
    {
        printf("\nUnable to open files 2 for reading...");
        return;
    }
    fscanf(file2,"%d",&size);
    for(int i = 0; i < size; i++)
    {
        dictionary[i] = (char*) malloc (MAX_LEN* sizeof(char));
        // fgets(dictionary[i],size,file2);
        // fscanf(file2,"%s",dictionary[i]);
        fgets (dictionary[i], MAX_LEN, file2);
        // if( fgets (dictionary[i], MAX_LEN, file2)!=NULL ) 
        // {
        // /* writing content to stdout */
        //     puts(dictionary[i]);
        // }
    }
    // printf("before get");
    fgets(string,MAX_LEN,file1);
    // printf("finish get");
    length = strlen(string);
    // printf("size %d",size);
    // printf("%d\n", length);
    fclose(file1); fclose(file2);

    for(int j = 0; j < length; j++)
    {
        words[j] = (char * ) malloc (MAX_LEN * sizeof(char));
        fscanf(file1,"%s",words[j]);
        // fgets(words[j],MAX_LEN,fioe);
        printf("%s",words[j]);
    }
    qsort(dictionary, MAX_LEN, sizeof(char*), compare);

    for (int i = 0; i < size; i++)
    {
        puts(dictionary[i]);
    }
    
    fclose(file1); 
    fclose(file2);
    // for(int i = 0; i < length; i++)
    // {
    //     printf("%s",*dictionary);
    // }
    // printf("finish scan file\n");
    // printf("%d", length);
    // distance = edit_distance(words[0],dictionary[0],0);
    // printf("%d",distance);
    for(int i = 0; i < length; i++)
    {
        distance = edit_distance(words[i],dictionary[0],0);
        // printf("before line");
        // printf("\n");
        printf("%d",distance);
        printf("\n--------------------\n");
        // for(int j = 0; j <= 19 ; j ++)
        // {
        //     printf("-");
        // }
        // printf("after line");
        // printf("\n");
        // printf("after line");
        // // printf("before count value");
        // // count = 1; arr[0] = 0;
        // printf("before for loop");
        for(int j = 0; j < size; j++)
        {
            temp = edit_distance(words[i],dictionary[j],0);
            arr[j] = temp;
            if(temp < distance)
            {
                distance = temp;
                arr[0] = j;
            }
            else if(temp == distance)
            {
                arr[count] = j;
                count ++;
            }
        }
        if (printOn == 1)
        {
            printf("\nCurrent word = %s", words[i]);
            printf("\nmin distance = %d\n", distance);
        }
        for(int j = 0; j < count; j++)
        {
            printf("\n%s\n", dictionary[arr[j]]);
        }
    }
    // printf("done");
}
