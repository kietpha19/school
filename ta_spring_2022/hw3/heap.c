#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>

#include "heap.h"  

#define DEBUG 1

//Finds the max value bettween the three numbers
int idxOfMaxValue(int *arr,int p,int left,int right,int N)
{
	//Makes sure to not go to deep		
	if(right<= N-1){
		//Checks if The top is the biggest, and then left or right.
		if(arr[p] >= arr[left] && arr[p] >= arr[right]){
			return p;
		}
		else if(arr[left]>=arr[right]){
			return left;
		}
		else{
			return right;
		}
	}
	//Makes sure that l is still seen just in case there is no right
	else if(left<=N-1){
		if(arr[left]>=arr[p]){
			return left;
		}
		else{
			return p;
		}
	}
	return p;
}


//This is sink down... I did not know it needed to be named heapify but it works! I DECIDED TO CHANGE IT UGGGH RE CODING
/*void heapify(int i, int N, int * arr){
} p = i 
*/
void heapify(int i,int N,int * arr)
{
	int p = i;
	//Variablies
	int left = (2*p)+1;
	int right = (2*p)+2;
	int sinker = arr[p];
	//Find the max value of the three
	int imv = idxOfMaxValue(arr,p,left,right,N);
	//Makes sures that P does not equal max value and does not coutnire past N
	while((imv!=p)&&(imv <=N))
	{
		//Changes the numbers around using sinker as the constatn
		arr[p] = arr[imv];
		arr[imv] = sinker;

		//Sets up to sink down again
		p=imv;
		left = (2*p)+1;
		right = (2*p)+2;
		imv = idxOfMaxValue(arr,p,left,right,N);
	}
}


//Runs sinkDown/heapify on all of the tree starting with the (N/2)-1
int * sortAHeap(struct heap_struct heapS, int * sz){

	int N = *sz;
	//Check if it is only two or less cause it causes issues other wise.
	if(((N/2)-1)==0){
		heapify(0,N,heapS.items);
	}


	//Runs sink down
	for(int p = ((N/2)-1); p>=0;p--){
		heapify(p,N,heapS.items);
	}
}


/*
0 = (unexpected) = Error
1 = * = remove()
2 = p/P = peek()
3 = VALUE = add()
4 = s/S = copy sorted from high to low
*/
int operationChoice(char choice)
{
	//Checks for a digit
	if(isdigit(choice) || choice=='-'){
		return 3;
	}
	//Checks for the rest
	else
	{
		if(choice == '*'){
			return 1;
		}
		else if(choice == 'p'||choice == 'P'){
			return 2;
		}
		else if(choice == 's'||choice == 'S'){
			return 4;
		}
		
		else{
			return 0;
		}
	}
}


//Creates a struct and runs heap sort afterwards. It creates the array here... So it is not a copy it return a copy of this heap
struct heap_struct make_heap(int N, int * arr){
	//Sets up heap and does a shallow copy

	struct heap_struct heap;
	heap.N = N;
	heap.capacity=N;

	heap.items = (int*)malloc(sizeof(int)*heap.N);

	for(int x=0;x<N;x++)
	{
		heap.items[x]=arr[x];
	}



	//Sorts heap
	sortAHeap(heap,&heap.N);

	return	heap;
}


//Prints out heap and all of its stuff
void print_heap(struct heap_struct heapS){
	printf("Heap:  size :%-3d, capacity :%-3d", heapS.N,heapS.capacity);

	printf("\nindexes:       ");
	for(int j=0;j<heapS.N;j++)
	{
		printf("%5d,",j);
	}

	printf("\nValues:        ");
	for(int k=0;k<heapS.N;k++)
	{
		printf("%5d,",heapS.items[k]);

	}
	printf("\n\n");

}


void add(struct heap_struct * heapP, int new_item){
	printf("added:%5d \n",new_item);
	heapP->N++;

	if(heapP->N > heapP->capacity)
	{
		heapP->items= (int*) realloc((int *)heapP->items, 2 * heapP->capacity * (sizeof(int)));


		heapP->capacity=heapP->capacity*2;
	}
	heapP->items[heapP->N-1]= new_item;

	sortAHeap(*heapP,&heapP->N);

}


//Takes a look at the top element / peak
int peek(struct heap_struct heapS){
	printf("Peak: %5d\n",heapS.items[0]);
	return heapS.items[0];
}


//Removes the top element and sorts
int poll(struct heap_struct * heapP){
	if(heapP->N == 0)
	{
		printf("Empty heap. no removed performed");
		return -1;
	}
	int removed = heapP->items[0];
	heapP->items[0]= heapP->items[heapP->N-1];
	heapP->N= (heapP->N)-1;
	sortAHeap(*heapP,&heapP->N);

	printf("Removed:%5d\n",removed);
	return removed;
}


//Creates a copy of the heap and makes it into a organized array
int* heap_sort(struct heap_struct heapS, int * sz){

	int length = heapS.N;
	int *copy = (int*)malloc(sizeof(int)*heapS.N);
	for(int x =0;x<length;x++){
		copy[x] = heapS.items[x];
	}

	//bIH is a copy of the biigest and length -1 so
	int biggestInHeap =copy[0];
	for(int a=length-1; a>0;a--)
	{
		biggestInHeap = copy[0];

		copy[0] = copy[a];
		//printf("biggestInHeap: %d     copy[0]: %d\n",biggestInHeap,copy[0]);
		heapify(0,a,copy);

		copy[a] = biggestInHeap;

	}

	printf("Sorted array : ");
	for(int b = 0; b<length;b++)
	{
		printf("%5d,",copy[b]);
	}
	printf("\n");
	free(copy);
}

void swim_up(int idx, int * arr){
	
}
/*
struct heap_struct make_heap_empty(int cap){

}


void destroy(struct heap_struct * heapP){
}
*/


