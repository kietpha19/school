#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct stack_struct{
    int array_size;
    int* stak;
    int top;
}



Stack;
typedef struct dynamic_array{
    int array_size;
    int e;
    int* array;
}

vector;
struct struct_graph{
    int node;
    int** matrix;
};

typedef struct struct_graph* graphPT;
int get_node_count(char* filename, char*** str_nodes){
    FILE* fp = fopen(filename, "r");

    if(!fp)
    { 
        printf("Could not open file %s. Exit\n", filename); 
        return -1; 
    }
    char line[200];

    char* token;
    int count = 0;
    int i;

   
    while (!feof(fp)){ fgets(line, 200, fp); count++; }

    fseek(fp, 0 , SEEK_SET);

    *str_nodes = (char**) malloc(sizeof(char*) * count);

    for(i = 0; i < count; i++){
        (*str_nodes)[i] = (char*) malloc(sizeof(char) * 31);
        if( (*str_nodes)[i] == NULL ) printf("ERROR OUT OF MEMORY\n");
        strcpy( (*str_nodes)[i], "" );
    }
    int n = 0;
    while(!feof(fp)){
        fgets(line, 1000, fp);

        token = strtok(line, " \n");

        strcpy( (*str_nodes)[n], token );
        n++;
    }
    fclose(fp);

    return count;
}



int** create_matrix(int rows, int columns){

    int i;

    int** matrix = (int**) malloc(sizeof(int*) * rows);





    for(i = 0; i < rows; i++)



    matrix[i] = (int*) malloc(sizeof(int) * columns);


    return matrix;
}

void free_matrix(int** array, int nodes){
    int i;
    for(i = 0; i < nodes; i++)
    free(array[i]);

    free(array);
}


graphPT create_graph(int nodes){
    int i,j;
    graphPT temp = malloc(sizeof(*temp));
    temp->node = nodes;
    temp->matrix = create_matrix(nodes, nodes);

    for(i = 0; i < nodes; i++)
    for(j = 0; j < nodes; j++)
    temp->matrix[i][j] = 0;
  
    return temp;
}

void free_graph(graphPT g){
    if(g == NULL) return;



    free_matrix(g->matrix, g->node);

    free(g);
}

void implement_edge(graphPT* g, int x, int y){



    (*g)->matrix[x][y] = 1;
}

int find_index(char** str_nodes, char* token, int nodes){
    int i;
    for(i = 0; i < nodes; i++){


        if( strcmp(str_nodes[i], token) == 0 ) return i;
    }

    return -1;
}

void free_char(char** words, int n){
    int i;
    for(i = 0; i < n; i++)
    free(words[i]);
    free(words);
}

void print_adjacency(graphPT graph)

{


    printf("\n\n");
    int i, j;


    int n = graph->node;

    printf("Adjacency matrix: \n");

    printf(" | ");


    for (i = 0; i < n; i++)


    printf("%d ", i);
    printf("\n");

    for(i = 0; i < n; i++)
    printf("------");
    printf("\n");

    for(i = 0; i < n; i++){
        printf(" %d|", i);
        for(j = 0; j < n; j++){
            printf(" %d", (graph->matrix)[i][j] );
        }
        printf("\n");
    }
}


void fread_file(char* filename, graphPT* g, char** str_nodes){
    FILE* fp = fopen(filename, "r");
    char line[2000];
    char* token;
    int i, nodes = (*g)->node;

    for (i = 0; !feof(fp); i++){
        fgets(line, 2000, fp);
        token = strtok(line, " \n");
            while(token != NULL){

                if( strcmp(str_nodes[i], token) != 0 ){


                    int j = find_index(str_nodes, token, nodes);
                    implement_edge(&(*g), j, i);
                }
                token = strtok(NULL, " \n");
            }

        }
  
        fclose(fp);
    }


    void stack_push(Stack* s, int item){
        if (s->top == (s->array_size - 1) ){
            printf("Stack is full\n");
            return;
        }
        s->top+=1;
        s->stak[s->top] = item;

    }

    int stack_pop(Stack* s){
        int num;
        if(s->top == -1){ printf("Stack is empty\n"); return -1; }
        else{
            num = s->stak[s->top];
            s->top= s->top - 1;
            return num;
        }
    }

    void visit_dfs(graphPT* g, Stack* s, vector* white, vector* grey, vector* black, int** d, int** f, int* matrix, int* time, int current, int* cycle){
  
        int j;
        *time = *time + 1;


        (*d)[current] = *time;


        grey->array[current] = 1;

        white->array[current] = 0;
        white->e = white->e - 1;

        int n = s->array_size - 1;

        
        int next [n];
        int next_size = 0;
        for(j = 0; j < n; j++)
        if ( (*g)->matrix[current][j] == 1){
            next[next_size] = j;
            next_size += 1;
        }

        for (j = 0; j < next_size; j++){

            int nei = next[j];

            if (black->e > 0 && (black->array[ nei ] == 1) ) continue;

            if (grey->e > 0 && (grey->array[ nei ] == 1) ) *cycle = 1;
  
            if(white->e > 0 && (white->array[ nei ] == 1))
            visit_dfs(g, s, white, grey, black, d, f, (*g)->matrix[nei], time, nei, cycle);
        }

  
        *time = *time + 1;
        (*f)[current] = *time;

        // move node at out of grey and into black state
        grey->array[current] = 0;
        black->array[current] = 1;

        
        stack_push(s, current);
    }


    void show (Stack *s){
        int i;
        if (s->top == -1){
            printf ("Stack is empty\n");
            return;
        }
        else{
            printf ("\n The status of the stack is: \n");
            for (i = s->top; i >= 0; i--) {
            printf ("%d)\t%d\n", i, s->stak[i]);
        }
    }
    printf ("\n");
}

int main(){

    

    graphPT graph;
    Stack stack;
    char** str_nodes;

    printf("This program will read, from a file, a list of courses and their prerequisites and will print the list in which to take cousres.\n");
    printf("Enter filename: ");
    char filename[31];
    scanf("%s", filename);

    int i;
    int number_nodes = get_node_count(filename, &str_nodes);

    if(number_nodes == 0 || number_nodes == -1){ printf("Failed to read in from file. Program will terminate.\n"); exit(EXIT_FAILURE); }


    printf("Number of vertices in built in graph: N = %d\n", number_nodes);


    printf("Vertex - coursename correspondence\n");


    for(i = 0; i < number_nodes; i++)

    printf("%d - %s\n", i, str_nodes[i]);
  

    graph = create_graph(number_nodes);

    fread_file(filename, &graph, str_nodes);

    print_adjacency(graph);

    

    stack.array_size = number_nodes + 1;

    stack.stak = (int*) malloc(sizeof(int) * stack.array_size);

    stack.top = -1;

    

    vector white;

    vector grey;

    vector black;

    white.array = (int*) malloc(sizeof(int) * number_nodes);

    white.array_size = number_nodes;


    white.e = number_nodes;

    grey.array = (int*) malloc(sizeof(int) * number_nodes);

    grey.array_size = number_nodes;

    grey.e = number_nodes;

    black.array = (int*) malloc(sizeof(int) * number_nodes);

    black.array_size = number_nodes;

    black.e = number_nodes;

    for (i = 0; i < number_nodes; i++){


        white.array[i] = 1;


        grey.array[i] = 0;


        black.array[i] = 0;
    }

    int time = 0;
    int* found = (int*) calloc(number_nodes, sizeof(int));



    int* complete = (int*) calloc(number_nodes, sizeof(int));

    
  
    int cycle = 0;
    for(i = 0; i < number_nodes && white.e > 0; i++)
    if(white.array[i] == 1)
    visit_dfs(&graph, &stack, &white, &grey, &black, &found, &complete, graph->matrix[i], &time, i, &cycle);
  
   
    printf("Start and finish times for each node, in format: \n");


    printf("node num: (start,finish)\n"); 

    for (i = 0; i < number_nodes; i++)
    printf("node %d: (%d, %d)\n", i, found[i], complete[i]);
  
    printf("\n");

    if(cycle)
    printf("There was at least one cycle. There is no possible ordering of the courses\n");
    else{
        printf("Order in which to take the courses:\n");
        for(i = 0; i < number_nodes; i++){
            int pop = stack_pop(&stack);
            printf("%d. - %s (corresponds to graph vertex %d\n", i+1, str_nodes[pop], pop);
        }
    }

    free(found);
    free(complete);

    free(white.array);


    free(grey.array);


    free(black.array);

    free(stack.stak);


    free_graph(graph);

    free_char(str_nodes, number_nodes);


    return EXIT_SUCCESS;
}
