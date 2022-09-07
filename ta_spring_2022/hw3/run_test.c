#include <stdlib.h>
#include <stdio.h>

#include "heap.h"  


/*struct heap_struct {
	int* items;
	int N;  // current size
	int capacity; // array capacity
*/


//THIS IS run_test.c Just prefered heap_client
void openFile() {
		//Startin variblies
    	char fname[100];
    	int N, i, count=0;
    	
    	FILE *fp;

    	// File stuff
    	printf("\nEnter the filename:");
    	scanf("%s", fname);
   		fp = fopen(fname, "r");
    	if (fp == NULL) {
    	    printf("File could not be opened.\n");
    	    return;
    	}
    	
    	//Grabbing numbs and setting up heap
		fscanf(fp, "%d", &N);		
		int nums1[N];
    	for (i = 0; i < N; i++) {

    		   fscanf(fp, "%d ", &nums1[i]);
    	}

    	struct heap_struct heap = make_heap(N,nums1);
    	
    	print_heap(heap);


		
    	// Setting operations up 

    	fscanf(fp, "%d", &N);
    	int numOfOps, operation;
    	char ops[100];

    	for(i = 0; i < N; i++)
    	{
    		fscanf(fp, "%s ", ops);
    		operation = operationChoice(ops[0]);
    		printf("Operation number: %d , string: %s\n",i+1,ops);
    		switch(operation){
    			case 1:
    			poll(&heap);
    			break;


    			case 2:
    			peek(heap);
    			break;


    			case 3:
    			add(&heap,atoi(ops));
    			break;


    			case 4:
    			heap_sort(heap, &heap.N);
    			break;


    			default :
    			printf("ERROR at : %d\n",i);
    		}

    		print_heap(heap);
    	}
         

    	//makeHeap //heap.items = (int*) malloc(sizeof(int)*N);

    	/*print_array(nums1, N);
    	bucket_sort(nums1, N);*/

    	//free(heap.items);
    	free(heap.items);
    	fclose(fp);
	}


//-------------------------------------------------------------

int main()
{
	printf("This program will create a max-heap and perform operations on it based on data from a file.\n");
	openFile();
	return 0;
}