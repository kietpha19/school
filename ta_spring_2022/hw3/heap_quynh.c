#include <stdlib.h>
#include <stdio.h>

#include "heap.h"  

#define DEBUG 1

/*
notes:
	heap starts at index 0, and the max index = size - 1
	we are using an array to represent a heap (binary tree where all children
	of a node are smaller in value than the node)
	the heap is arranged so that it is a "complete" heap
*/

// creates an empty heap with capacity cap
struct heap_struct make_heap_empty(int cap){
	int *arr = malloc(cap * sizeof(int));
	struct heap_struct heap;
	heap.capacity = cap;
	heap.N = 0;
	heap.items = arr;
	return heap;
}

// converts an unsorted array into a heap
struct heap_struct make_heap(int N, int * arr){
	struct heap_struct heap;
	heap.items = arr;
	heap.N = N;
	heap.capacity = N;
	// start at the rightmost node with height 1 and sort it using heapify
	// then proceed towards the left and up
	for (int p = (N-2)/2; p >= 0; p--) {
		heapify(p, N, heap.items);
	}
	return heap;
}

// destroys a heap by freeing the array and setting the size and cap to 0
void destroy(struct heap_struct * heapP){
	if (heapP->items != NULL) {
		free(heapP->items);
		heapP->items = NULL; // need to set it to null to check if arr is freed
	}
	heapP->N = 0;
	heapP->capacity = 0;
}

// prints the contents of a heap with its respect index in the array
// prints top->bottom, left-> right (increasing index)
void print_heap(struct heap_struct heapS){
	printf("Heap:  size: %d, capacity: %d\n", heapS.N, heapS.capacity);
	printf("indexes:      ");
	for (int i = 0; i < heapS.N; i++) {
		printf("%6d,", i);
	}
	printf("\nvalues:       ");
	for (int i = 0; i < heapS.N; i++) {
		printf("%6d,", heapS.items[i]);
	}
	printf("\n\n");
}

// the opposite of sink down
// brings a node up the heap until all of its children are smaller than it
void swim_up(int idx, int * arr){
	// (idx - 1)/2 = index of parent node
	// if parent node is smaller than current node, swap the nodes
	while ((idx > 0) && (arr[idx] > arr[(idx - 1)/2])) {
		int temp = arr[idx];
		arr[idx] = arr[(idx - 1)/2];
		arr[(idx - 1)/2] = temp;
		idx = (idx - 1)/2;
	}
}

// helper function for heapify
// finds the index of the max value given a node and its children
int idxOfMaxValue(int *arr, int i, int left, int right, int N) {
	int imv = i; // so far the given node is the max value
	if (left < N && arr[left] > arr[imv]) imv = left;
	if (right < N && arr[right] > arr[imv]) imv = right;
	return imv;
}

// aka sink_down()
// "sinks" a node down to its proper spot in the heap by making swaps with
// children nodes that have a higher value than it
void heapify(int i, int N, int * arr){
	int left = 2 * i + 1;
	int right = 2 * i + 2;
	int p = i;
	int imv = idxOfMaxValue(arr, p, left, right, N);
	while (imv != p && imv < N) {
		int temp = arr[imv];
		arr[imv] = arr[p];
		arr[p] = temp;
		p = imv;
		left = 2*p + 1;
		right = 2*p + 2;
		imv = idxOfMaxValue(arr, p, left, right, N);
	}
}

// inserts a value into the heap
void add(struct heap_struct * heapP, int new_item){
	// double the heap's capacity if it is full
	if (heapP->N == heapP->capacity) {
		heapP->items = realloc(heapP->items, (heapP->capacity)*2*sizeof(int));
		heapP->capacity = 2*(heapP->capacity);
		printf("\nresizing\n");
	}
	// put the new value at the last position in the heap, and make it "swim up"
	// to its proper position in the heap
	heapP->items[heapP->N] = new_item;
	swim_up(heapP->N, heapP->items);
	heapP->N = heapP->N + 1; // increase the size of the heap
}

// returns the max value in the heap but don't remove it
int peek(struct heap_struct heapS){
	return heapS.items[0];
}

// returns the max value in the heap and also removes it from the heap
int poll(struct heap_struct * heapP){
	int max = heapP->items[0];
	int size = heapP->N;
	// can't poll if heap is empty
	if (size == 0) {
		printf("Empty heap. No remove performed.");
		return 0;
	}
	// to remove the max value (the top value),
	// move the last value in the heap to the top. then, decrease the heap size 
	// by 1. lastly, sink down the top value (heapify) to its proper spot
	heapP->items[0] = heapP->items[size-1];
	heapP->N = heapP->N - 1;
	heapify(0, size, heapP->items);
	return max;
}

// sorts the array in place in the heap by continuously "polling" the heap without
// actually decreasing the heap size and removing the max value
// then, copy the sorted array to a new dynanamically allocated array
// lastly, remake the sorted array into a heap (same algorithm as in make_heap()),
// and return the copy of the sorted array
int* heap_sort(struct heap_struct heapS, int * sz){
	*sz = heapS.N;
	int N = heapS.N;
	
	// sorting the array in the heap
	// works kind of like bubble sort, where the largest value goes to the end,
	// but takes only O(lgN) time for each iteration because of the heap's shape
	for (int i = N - 1; i >= 1; i--) {
		int temp = heapS.items[0];
		heapS.items[0] = heapS.items[i];
		heapS.items[i] = temp;
		N = N - 1; // notice how we're not really decreasing the heap's size
		heapify(0, N, heapS.items);
	}
	N = heapS.N; // resetting N to be the actual size of the heap (hasn't changed)
	// making a copy of the sorted array in the heap struct
	int *arr = malloc(N * sizeof(int));
	for (int i = 0; i < N; i++) {
		arr[i] = heapS.items[i];
	}

	// remake the sorted array in the heap struct into an actual heap
	for (int p = (N-2)/2; p >= 0; p--) {
		heapify(p, N, heapS.items);
	}
	return arr;
}

