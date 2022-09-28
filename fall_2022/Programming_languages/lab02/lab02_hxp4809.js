/*name: Hoang Anh Kiet Pham
 * id : 1001904809
 * due date: Oct 4th, 2022
 */

//task 1
const inputtable = [1,2,3,4,5,6,7,8,9,10];
console.log("task 1: ");
console.log(inputtable)
console.log();

//task 2a
const mult = x => y => x*y;
const mult5 = mult(5);
const fiveTable = inputtable.map(mult5);
console.log("task 2a: ");
console.log(fiveTable);
//task 2b
const mult13 = mult(13);
const thirteenTable = inputtable.map(mult13);
console.log("task 2b: ");
console.log(thirteenTable);
//task 2c
const square = x => x*x;
const squareTable = inputtable.map(square);
console.log("task 2c: ");
console.log(squareTable);
console.log();


//task 3 - for this task, we are assuming the range is always (0,100)
const isOdd = x => x%2==1;
//using recursion
function get_odd_in_multFive(start, end, count){
    if(start > end){
        return;
    }
    else if (isOdd(start)){
        console.log("%d: %d", count, start)
        get_odd_in_multFive(start+5, end, count+1)
    }
    else{
        get_odd_in_multFive(start+5, end, count)
    }
    
}
console.log("task 3 using recursion: ")
get_odd_in_multFive(0,100,1);
console.log();

//task 3 if the solution requires store the result in a list (using recursion)
function get_odd_in_multFive_list(start, end, result){
    if(start > end){
        return result;
    }
    else if (isOdd(start)){
        //again, concate is an pure function, so there is no side effect
        return get_odd_in_multFive_list(start+5, end, result.concat([start]));
    }
    return get_odd_in_multFive_list(start+5, end, result);
}
const odd_in_multFive_list = get_odd_in_multFive_list(0, 100, []);
console.log("task 3 using recursion and return a list: ")
console.log(odd_in_multFive_list);
console.log();

//task 3 if use map and filter
const add = x => y => x+y;
const add10 = add(10);
//concat is a pure function, so it gurantees that there is no side effect
const inputtable_fix = inputtable.concat(inputtable.map(add10)); 
const fiveTable_task3 = inputtable_fix.map(mult5);
const odd_in_fiveTable = fiveTable_task3.filter(isOdd);
console.log("task 3 if use map and filter: ")
console.log(odd_in_fiveTable);
console.log();

//task 4 - for this task we are assuming the range is always (0,100)
const isEven = x => x%2==0;
//using recursion
function get_sum_of_even_in_multSeven(start, end, sum){
    if(start > end){
        return sum;
    }
    else if (isEven(start)){
        return get_sum_of_even_in_multSeven(start+7, end, sum+start);
    }
    else{
        return get_sum_of_even_in_multSeven(start+7, end, sum);
    }
}
const sum_even_in_sevenTable_recursion = get_sum_of_even_in_multSeven(0,100,0);
console.log("task 4 using recursion");
console.log(sum_even_in_sevenTable_recursion);
console.log();

//task 4 if use map, filter and reduce
const sevenTabe = inputtable_fix.map(mult(7));
const even_in_senvenTable = sevenTabe.filter(x => (isEven(x) && x<100));
const sum_even_in_sevenTable = even_in_senvenTable.reduce((a,b)=>a+b);
console.log("task 4 using map, filter, and reduce");
console.log(sum_even_in_sevenTable);
console.log();


//task 5
const cylinder_volume = r => h => 3.14*r*r*h;
console.log("task 5: ")
console.log(cylinder_volume(5)(10));
console.log(cylinder_volume(5)(17));
console.log(cylinder_volume(5)(11));
console.log();

//task 6
const makeTag = function(beginTag, endTag){ 
    return function(textcontent){ 
       return beginTag +textcontent +endTag; 
    } 
} 
const makeTag_table = makeTag("<table>\n", "</table>\n");
const makeTag_tr = makeTag("<tr>\n", "</tr>\n");
const makeTag_th = makeTag("<th>", "</th>\n");
const makeTag_td = makeTag("<td>", "</td>\n");

const head1 = makeTag_th("FirstName");
const head2 = makeTag_th("LastName");
const head3 = makeTag_th("Age");
const table_header = makeTag_tr(head1+head2+head3);

const person1 = makeTag_td("Hailey") + makeTag_td("Nguyen") + makeTag_td("21");
const row1 = makeTag_tr(person1);

const person2 = makeTag_td("Dania") + makeTag_td("Mendez") + makeTag_td("18");
const row2 = makeTag_tr(person2);

const person3 = makeTag_td("Jasmine") + makeTag_td("Luu") + makeTag_td("23");
const row3 = makeTag_tr(person3);

const html_table = makeTag_table(table_header + row1 + row2 + row3);

console.log("task 6: ");
console.log(html_table);


//bonus: genetic version of task 3 and 4

//for grader to choose different multiplier and range
const mult_num = 3; 
const start = 0;
const end = 100;
const even = 0;
const odd = 1;

//task 3 - genetic version
function get_even_or_odd_in_multNum_table(start, end, mult_num, cond, result){
    function recursion(s){
        if(s > end){
            return result;
        }
        else if (cond(s)){
            result.push(s);
        }
        return recursion(s+mult_num);
    }
    return recursion(start- (start%mult_num) + mult_num);
}
const result = get_even_or_odd_in_multNum_table(start,end,mult_num,isOdd,[]);
console.log(result);


