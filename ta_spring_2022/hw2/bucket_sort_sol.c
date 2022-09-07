/* 
 * Updated 2/25/2021 - Alexandra Stefan
 */

#include <stdlib.h>
#include <stdio.h>
#include <math.h>

#include "list.h"


/* 
compile with -g to collect debugging info needed for Valgrind: 
gcc -g bucket_sort.c list.c

run with Valgrind:
valgrind --leak-check=full --show-leak-kinds=all ./a.out

if the above fails, you can run it without the --show-leak-kinds=all, so use only:
valgrind --leak-check=full ./a.out

run without Valgrind:
./a.out
*/

void print_array(int arr[], int N);
nodePT insert_sorted(nodePT L, nodePT newP);

void print_array(int arr[], int N){
	int j;
	printf("\n array: ");
	for(j= 0; j<N; j++){
		printf("%5d,", arr[j]);
	}
	printf("\n");
}

void bucket_sort(int arr[], int N){
	if (N==0) return;
	int min, max;
	min = arr[0];
	max = arr[0];
	int j, idx;
	for(j=1; j<N; j++){
		if (min > arr[j]) {
			min = arr[j];
		}
		if (max < arr[j]) {
			max = arr[j];
		}
	}
	printf("\nBucketsort: min=%d, max = %d, N=%d buckets\n", min, max, N);
	// use N buckets;
	nodePT buckets[N];
	for(j=0; j<N; j++){
		buckets[j] = NULL;
	}
	
	double diff = ((double)max)-min+1;
	nodePT newP = NULL;
	for(j=0; j<N; j++){
		idx = floor(((arr[j] - (double)min)/(diff))*N);
		printf("arr[%d]=%5d, idx = %d\n", j, arr[j], idx);
		newP = new_node(arr[j]);
		buckets[idx] = insert_sorted(buckets[idx], newP);
	}
	
	int ka;
	for(j=0, ka=0; j<N; j++){
		nodePT curr = buckets[j];
		printf("------ List at index %d : ", j);
		print_list_horiz(buckets[j]);
		while(curr!= NULL){
			arr[ka] = curr->data;
			ka++;
			curr = curr->next;
		}
	}
	
	for(j = 0; j<N; j++){
		destroy_list(buckets[j]);
	}
}

nodePT insert_sorted(nodePT L, nodePT newP){
	if (L == NULL) { return newP;  }// no link updates needed 
	else {
		nodePT prev = NULL;  // this will be the node before newP
		nodePT after = L;    // this will be the node after newP
		while ((after!=NULL) && (newP->data >= after->data)) {
			prev = after;
			after = after->next;
		}
		newP->next = after;
		if (prev == NULL) { // insert as new head
			return newP;
		}
		else {
			prev->next = newP;
			return L;
		}
	}
}


//-------------------------------------------------------------

int * read_file(int *N){
	int j;
	FILE *fp;
	char fname[101];
	printf("\nEnter the filename: ");
	scanf("%s", fname);
	fp =fopen(fname, "r");
	if (fp == NULL){
		printf("File could not be opened.\n");
		return NULL;
	}
	fscanf(fp, "%d", N);

	int* nums1 = calloc(*N, sizeof(int) );

	// read from file and populate array
	for (j = 0; j < *N; j++) {
		fscanf(fp, "%d ", &nums1[j]);
		//printf("%4d|", nums1[j]);
	}	
	fclose(fp);
	return nums1;
}

void run1(){
   int N;
   int* arr = read_file(&N);
   if (arr == NULL) { return;}
   
   print_array(arr, N);
   bucket_sort(arr, N);
   print_array(arr, N);
   
   free(arr);
}

int main()
{
	printf("This program will read a file name, load data for an array from there and print the sorted array.\n");
	printf("The array is sorted using bucket sort.\n");
	printf("This will be repeated as long as the user wants.\n");
	int option;
	do {
		run1();
		printf("\nDo you want to repeat? Enter 1 to repeat, or 0 to stop) ");
		char ch;
		scanf("%d%c",&option, &ch);  // ch is used to remove the Enter from the input buffer
	} while (option == 1);

   return 0;
}
