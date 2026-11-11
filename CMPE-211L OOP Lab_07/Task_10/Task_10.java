import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

public class Task_12 {
    public static void main(String[] args) throws IOException {
        File myfile = new File("abc.txt");
        myfile.createNewFile();
        FileWriter fileWrite = new FileWriter("abc.txt");
        fileWrite.write("anaya");
        fileWrite.close();
//        myfile.delete();
    }
}
