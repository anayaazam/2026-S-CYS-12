import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
class Main {
    public static void main(String[] args) throws IOException {
        File myfile = new File("abc.txt");
        myfile.createNewFile();
        FileWriter fileWrite = new FileWriter("abc.txt");
        fileWrite.write("anaya");
        myfile.close();
        myfile.delete();

    }
}


