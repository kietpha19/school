#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "spell.h"

#define MAX_LEN 100 // max length of a word
#include <ctype.h> // for tolower();

/*  Suggestions
- When you work with 2D arrays, be careful. Either manage the memory yourself, or
work with local 2D arrays. Note C99 allows parameters as array sizes as long as
they are declared before the array in the parameter list. See:
https://www.geeksforgeeks.org/pass-2d-array-parameter-c/

Worst case time complexity to compute the edit distance from T test words
to D dictionary words where all words have length MAX_LEN:
Student answer: Theta((T*D)*(MAX_LEN)^2)


Worst case to do an unsuccessful binary search in a dictionary with D words, when
all dictionary words and the searched word have length MAX_LEN
Student answer: Theta(lg(D)*MAX_LEN)
*/


/* Helper Functions */
// prints the array used to calculate the edit distance between "first string" and "second_string"
void print_array(int row, int col, int arr[row][col], char * first_string, char * second_string) {
    printf("\n");
    for (int i = 0; i < row; i++) {
        if (i == 0) {
            printf("  |   |");
            for (int j = 0; j < col-1; j++) printf("%3c|", second_string[j]);
            printf("\n---");
            for (int j = 0; j < col; j++) printf("----");
            printf("\n");
        }
        for (int j = 0; j < col; j++) {
            if (j == 0) {
                if (i < 1) printf("  |");
                else printf("%2c|", first_string[i-1]);
            }
            printf("%3d|", arr[i][j]);
        }
        printf("\n---");
        for (int j = 0; j < col; j++) printf("----");
        printf("\n");
    }
    printf("\n");
}

/*
Parameters:
    first_string - pointer to the first string (displayed vertical in the table)
    second_string - pointer to the second string (displayed horizontal in the table)
    print_table - If 1, the table with the calculations for the edit distance will be printed.
                  If 0 (or any value other than 1)it will not print the table
    (See sample run)
Returns: the value of the edit distance (e.g. 3)
*/
int edit_distance(char * first_string, char * second_string, int print_table) {
    int length1 = strlen(first_string) + 1;
    int length2 = strlen(second_string) + 1;
    int arr[length1][length2];

    for (int i = 0; i < length1; i++) {
        for (int j = 0; j < length2; j++) {
            if (i == 0) arr[i][j] = j;
            else if (j == 0) arr[i][j] = i;
            else {
                int min = arr[i-1][j] + 1;
                if (min > arr[i][j-1] + 1) min = arr[i][j-1] + 1;
                if (first_string[i-1] == second_string[j-1]) {
                    if (min > arr[i-1][j-1]) min = arr[i-1][j-1];
                } else if (min > arr[i-1][j-1] + 1) min = arr[i-1][j-1] + 1;

                arr[i][j] = min;
            }
        }
    }

    // if user has on verbose mode, print the table used to calculate the edit distance
    if (print_table) print_array(length1, length2, arr, first_string, second_string);
	return arr[length1-1][length2-1];
}

// compare function for qsort, used to help sort the dictionary in lexicographical order
int str_compare(const void* a, const void* b) {
    const char** stringA = (const char**)a;
    const char** stringB = (const char**)b;
    return (strcmp(*stringA, *stringB));
}

// prints every word in the dictionary along with a counter by each word
void print_dictionary_helper(char** dictionary, int size) {
    for (int i = 0; i < size; i++) printf("%d. %s\n", i, dictionary[i]);
}

// prints dictionary before and after sorting alphabetically. called when in verbose mode
void print_dictionary(char** dictionary, int size) {
    printf(" Original dictionary:\n");
    print_dictionary_helper(dictionary, size);
    qsort(dictionary, size, sizeof(char*), str_compare);
    printf("\n Sorted dictionary (alphabetical order):\n");
    print_dictionary_helper(dictionary, size);
    printf("\n");
}

// reads from file and reads words into an array of pointers to chars.
char** createDictionary(char* dictname, int *size) {
    FILE *fp = fopen(dictname, "r");
    if (fp == NULL) {
        printf("Could not open file %s. Exit\n", dictname);
        return NULL;
    }

    char numWords[MAX_LEN+1];
    fgets(numWords, MAX_LEN, fp);
    *size = atoi(numWords);

    char** dictionary = malloc((*size)*sizeof(char *));

    printf("Loading the dictionary file: %s\n\n", dictname);
    printf("Dictionary has size: %d\n", *size);
    for (int i = 0; i < (*size); i++) {
        dictionary[i] = malloc((MAX_LEN+1)*sizeof(char));
        fgets(dictionary[i], MAX_LEN, fp);
        int length = strlen(dictionary[i]);
        dictionary[i][length-1] = 0;
    }

    fclose(fp);
    return dictionary;
}

void deleteDictionary(char *** dictionary, int size) {
    for (int i = 0; i < size; i++) free((*dictionary)[i]);
    free(*dictionary);
}

/*
Description: searches dictionary for word. also keeps track of how many words were compared. helper function for check_word
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
Returns -1 if word not found, or the index of the word in the dictionary if it is found
*/
int binary_search(char* word, char** dictionary, int left, int right, int printOn, int* count) {
    if (right < left) return -1;
    (*count)++;
    int index = (left + right) / 2;

    if (printOn) printf("dict[%d] = %s\n", index, dictionary[index]);
    if (strcmp(word, dictionary[index]) == 0) return index;
    if (strcmp(word, dictionary[index]) < 0) return binary_search(word, dictionary, left, index-1, printOn, count);
    if (strcmp(word, dictionary[index]) > 0) return binary_search(word, dictionary, index+1, right, printOn, count);
}

/* Description: checks if word exists in dictionary using binary search
 * Returns 1 for found, 0 for not found */
int check_word(char* word, char** dictionary, int size, int printOn, int* count) {
    if (printOn) printf("Binary search for: %s\n", word);
    int index = binary_search(word, dictionary, 0, size-1, printOn, count);

    // found word, return true
    if (index != -1) {
        return 1;
    } else {
        if (printOn) printf("Not found\n\n");
        return 0;
    }
}

/*
Description: calculates edit distance for every word in the dictionary vs given word and stores the indices of
the words with the lowest edit distance in a dynamic array

Parameters:
    word -  the word to find suggestions for, using edit_distance()
    dictionary - a list of "valid" words in our language, used to find suggestions for invalid words
    size = size of dictionary (int)
    numSug = used to store size of the array we're returning

Returns: an int array contain the indexes of all the strings in the dictionary that have the lowest edit distance
    when compared with word
*/
int* find_suggestions(char* word, char** dictionary, int size, int* numSug) {
    int min;
    int* suggestions; // array of indexes of the strings (in the dictionary) with lowest edit_distance w/ word

    // calculate edit distance for every word in dictionary, save the indexes of words with lowest edit_distance
    // into suggestions
    for (int i = 0; i < size; i++) {
        int ed = edit_distance(word, dictionary[i], 0);
        // fist word, by default it has the lowest edit distance, so save it to suggestions
        if (i == 0) {
            min = ed;
            suggestions = malloc(sizeof(int));
            suggestions[0] = i;
            *numSug = 1;
        } else if (ed < min) {
            // found a smaller edit distance, so erase all words in suggestions and add the new word
            min = ed;
            *numSug = 1;
            suggestions = realloc(suggestions, sizeof(int));
            suggestions[0] = i;
        } else if (ed == min) {
            // found another word with same current min edit distance, so add it to suggestions
            (*numSug)++;
            suggestions = realloc(suggestions, (*numSug)*sizeof(int));
            suggestions[*numSug-1] = i;
        }
    }
    printf("     Minimum distance: %d  (computed edit distances: %d)\n", min, size);
    return suggestions;
}

// prints the array of words with the lowest edit distance (for the menu)
void print_suggestions(int* suggestions, int size, char** dictionary) {
    printf("     Words that give minimum distance:\n");
    for (int i = 0; i < size; i++) printf(" %d - %s\n", i+1, dictionary[suggestions[i]]);
}

/*
    reads testfile, parses words, and checks if the words are in the dictionary (using check_word())
    if not in dictionary, it calculates the edit distance and generates the array of suggestions
*/
void process_testfile(char* testname, char** dictionary, char* outputfile, int size, int printOn) {
    FILE *fp = fopen(testname, "r");
    if (fp == NULL) {
        printf("Could not open file %s. Exit\n", testname);
        return;
    }

    char word[MAX_LEN+1];
    FILE *of = fopen(outputfile, "w");
    char c;

    while ((c = getc(fp)) != EOF && c != '\n') {
        if (c == ' ' || c == ',' || c == '!' || c == '?' || c == '.') {
            putc(c, of); // writing separator characters, as is, to the output file
        } else {
            // not a separator character, so it must be a word
            word[0] = c;
            int i = 1;
            // reading in letters into the string 'word' until it encounters another separator
            while ((c = getc(fp)) != EOF && (c != ' ' && c != ',' && c != '!' && c != '?' && c != '.')) word[i++] = c;

            word[i] = 0; // adding null-terminator
            char wordcopy[i];
            strcpy(wordcopy, word);
            for (int j = 0; j < i; j++) wordcopy[j] = tolower(wordcopy[j]); // converting word to all lowercase

            int count = 0;
            if (check_word(wordcopy, dictionary, size, printOn, &count)) { // word was found in dictionary, write to file as is
                printf("---> |%s| (words compared when searching: %d)\n     - OK\n\n\n", word, count);
                fputs(word, of);
            } else { // word was not found in dictionary, calculate edit distance
                printf("---> |%s| (words compared when searching: %d)\n-1 - type correction\n", word, count);
                printf(" 0 - leave word as is (do not fix spelling)\n");

                int* suggestions;
                int numSug = 0;
                suggestions = find_suggestions(wordcopy, dictionary, size, &numSug);
                print_suggestions(suggestions, numSug, dictionary);

                printf("Enter your choice (from the above options): ");
                int choice;
                char newline; // newline

                while (1) {
                    scanf("%d%c", &choice, &newline);

                    if (choice == -1) { // user enters their own correction
                        char correctWord[MAX_LEN+1];
                        printf("Enter the correct word: ");
                        scanf("%s", correctWord);
                        fputs(correctWord, of);
                        break;
                    } else if (choice == 0) { // keep word as is
                        fputs(word, of);
                        break;
                    } else if (choice <= numSug) { // correct word to one of the suggestions displayed
                        fputs(dictionary[suggestions[choice-1]], of);
                        break;
                    }
                    else printf("Invalid input.\nEnter your choice (from the above options): ");
                }
                printf("\n");
                free(suggestions);
            }
            putc(c, of); // because an extra char was read to exit the while loop
        }
    }
    fclose(of);
    fclose(fp);
}

void spell_check(char * testname, char * dictname, int printOn) {
    int size; // size of dictionary

    // creating output filename string
    char outputfile[strlen(testname) + 5];
    strcpy(outputfile, "out_");
    strcat(outputfile, testname);
    printf("Corrected output filename: %s\n\n", outputfile);

    // creating and sorting dictionary
    char** dictionary = createDictionary(dictname, &size);
    if (dictionary == NULL) return;
    // print_dictionary also sorts the dictionary, so no need to recall qsort here
    if (printOn) print_dictionary(dictionary, size);
    else qsort(dictionary, size, sizeof(char*), str_compare);

    // check each word in test file to see if it is valid according to the dictionary
    process_testfile(testname, dictionary, outputfile, size, printOn);

    deleteDictionary(&dictionary, size);
}
