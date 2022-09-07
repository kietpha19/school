/*
 * Name: Hoang Anh Kiet Pham
 * ID: 1001904809
 * language version: jdk version 14.0.2
 * OS: Ubuntu (UTA virtual machine)
 */
import java.io.File;

public class hxp4809_lab01{
    
    public static void main(String[] args){
        long total = 0;
        String path_name = System.getProperty("user.dir"); 
        total = get_total_size_of_dir(path_name);
        System.out.println(total);
    }

    /*
     * this function is to get the total size of the current working directory
     * it takes the path of the directory as parameter,
     * then loop through every entry in that directory
     *     if the entry is a file:
     *         add its size to sum
     *     else:
     *         make the path to the child directory by simply add / and the directory name
     *         recursively call the function passing the path of child dir to it
     * return the sum
     */
    private static long get_total_size_of_dir(String path_name){
        File dir = new File(path_name);
        File[] entries = dir.listFiles();
        long sum = 0;
        for(File entry : entries){
            if(entry.isFile()){
                //System.out.println("file: " + entry.getName()); //for debug 
                sum += entry.length();
            }
            else{
                //System.out.println("dir: " + entry.getName()); //for debug
                String child_path_name = path_name + "/" + entry.getName();
                sum += get_total_size_of_dir(child_path_name);
            }
        }
        return sum;
     }

}