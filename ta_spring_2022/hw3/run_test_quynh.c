#include <stdlib.h>
#include <stdio.h>
#include "heap.h"
#include <string.h>

// prints the contents of a heap sorted smallest->largest
void sort(struct heap_struct heap) {
	int sz = 0;
	int * sorted_array = heap_sort(heap, &sz);
	printf("sorted array: ");
	for(int i=0; i < sz; i++) { 
		printf("%6d, ", sorted_array[i] );  
	}   
	printf("\n");
	free(sorted_array);
}

// helper function to parse the instruction line of the data file
void parse_instruction(char *ins, struct heap_struct *heap) {
	if (strcmp(ins, "S") == 0 || strcmp(ins, "s") == 0) {
		sort(*heap);
	} else if (strcmp(ins, "P") == 0 || strcmp(ins, "p") == 0) {
		printf("Peek: %9d\n", peek(*heap));
	} else if (strcmp(ins, "*") == 0) {
		printf("Removed: %6d\n", poll(heap));
	} else {
		printf("Add: %9d\n", atoi(ins));
		add(heap, atoi(ins));
	}
	// print the heap after every instruction to see any updates
	print_heap(*heap);
}

int main() {
	int N, P; // N = number of values in array, P = number of instructions
	FILE *fp;
	char fname[101];
	char instruction[10];
	printf("\nEnter the filename: ");
	scanf("%s", fname);

	// checking if file exists
	fp =fopen(fname, "r");
	if (fp == NULL){
		printf("File could not be opened.\n");
		return 0;
	}

	// reading values from file and storing it in a dynamically allocated array
	fscanf(fp, "%d ", &N);
	int* nums = calloc(N, sizeof(int));
	for (int j = 0; j < N; j++) {
		fscanf(fp, "%d ", &nums[j]);
	}

	// make a heap struct from the array
	struct heap_struct heap = make_heap(N, nums);
	print_heap(heap);

	// read and execute each instruction one-by-one
	fscanf(fp, "%d ", &P);
	// read and execute instructions
	for (int j = 0; j < P; j++) {
		fscanf(fp, "%s", instruction);
		printf("Operation number %d, string: %s\n", j+1, instruction);
		parse_instruction(instruction, &heap);
	}	

	// freeing memory
	destroy(&heap);
	fclose(fp);
}