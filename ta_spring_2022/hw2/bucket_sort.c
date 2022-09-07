/* 
 * Updated 2/17/2022 - Alexandra Stefan
 */
/*
*Taduri Sri Archana- sxt4029
*Yeshwa Sri - yxt6881
*/

#include <stdlib.h>
#include <stdio.h>
#include <math.h>

#include "list.h"

struct bucket
{
    int c;
    int* val;
};

int comint(const void* f, const void* s)
{
    int a = *((int*)f), b =  *((int*)s);
    if (a == b)
    {
        return 0;
    }
    else if (a < b)
    {
        return -1;
    }
    else
    {
        return 1;
    }
}


/* 
compile with -g to collect debugging info needed for Valgrind: 
gcc -g bucket_sort.c list.c

run with Valgrind:
valgrind --leak-check=full --show-leak-kinds=all ./a.out

run without Valgrind:
./a.out
*/

void print_array(int arr[], int N);

/* // recommended helper functions:
// function to insert a new node in a sorted list.
nodePT insert_sorted(nodePT L, nodePT newP);
//  function to sort an array sing bucket sort
void bucket_sort(int arr[], int N)
*/

void print_array(int arr[], int N)
{
	int k;
	printf("\n array: ");
	for(k= 0; k<N; k++)
	{
		printf("%5d,", arr[k]);
	}
	printf("\n");
}



void run1(long long int arr[],int n)
{
    struct bucket buckets[n];
    int i, j, k;
    long long int max,min;
    long long int index[n];
    max=arr[0];
    min=arr[0];
    for (j = 0; j < n; j++)
    {
        buckets[j].c = 0;
        buckets[j].val = (int*)malloc(sizeof(int) * n);
    }
    for(j=0;j<n;j++)
	{
            if(arr[j] > max)
        {
            max = arr[j];
        }


        if(arr[j] < min)
        {
            min = arr[j];
        }
    }
     printf("The array:");
     for(j=0;j<n;j++){
            printf("%lld ",arr[j]);
     }
     printf("\nBucketsort: max=%lld min=%lld N=%d buckets\n",max,min,n);
     for(j=0;j<n;j++)
	 {
        index[j]=(arr[j]*n)/(max+1);
        if(index[j]<100 && index[j]>=0)
		{
        printf("a[%d]= %lld index=%lld\n",i,arr[j],index[j]);
        }
        if(index[i]>100)
		{
            printf("a[%d]= %lld index=%lld\n",i,arr[j],index[j]/100);
        }
        if(index[i]<0)
		{
            printf("a[%d]= %lld index=%lld\n",i,arr[j],index[j]==0);
        }

     }


    for (j = 0; j < n; j++)
    {

        if (arr[j] < 0 )
        {
            buckets[0].val[buckets[0].c++] = arr[i];
        }
        else if (arr[j] > 10)
        {
            buckets[2].val[buckets[2].c++] = arr[j];
        }
        else
        {
            buckets[1].val[buckets[1].c++] = arr[j];
        }
    }
    for (k = 0, i = 0; i < n; i++)
    {
        // now using quicksort to sort the elements of buckets
        qsort(buckets[i].val, buckets[i].c, sizeof(int), &comint);
        for (j = 0; j < buckets[i].c; j++)
        {
            arr[k + j] = buckets[i].val[j];
        }
        k += buckets[i].c;
        free(buckets[i].val);
    }
  
}

int main()
{
	printf("This program will read a file name, load data for an array from there and print the sorted array.\n");
	printf("The array is sorted using bucket sort.\n");
	printf("This will be repeated as long as the user wants.\n");
        char f1[100];
        int N, z, k, n;
        FILE *fp;
        int option;

	do {
                 printf("filename: ");
                 scanf("%s", f1);
                 fp =fopen(f1, "r");
                 if (fp == NULL){
                 printf("File could not be opened.\n");
        return 1;
        }
        fscanf(fp,"%d", &N);
        long long int numb[N];
        n=N;
        for (z = 0; z < N; z++) {
        fscanf(fp,"%lld ", &numb[z]);
       
        }
        long long int *arr=numb;
       

		run1(arr, n);
                printf("array:");
                for(k=0;k<N;k++)
                printf("%lld, ", numb[k]);
		printf("\nDo you want to repeat? Enter 1 to repeat, or 0 to stop) ");
		scanf("%d",&option);
	} 
        while (option == 1);
   return 0;
}

