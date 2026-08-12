package xyz.retrixe;

import java.io.*;
import java.util.*;

public class second {

    public static List<List<String>> list = new ArrayList<>();

    public static void machinecode(Scanner sc){
        while(sc.hasNextLine()){
            List<String> list1 = new ArrayList<>();
            String line = sc.nextLine().trim();
            String[] arr = line.split(" ");
            for(int i=0;i<arr.length;i++){
                if(arr[i].matches("\\d+")){
                    list1.add(arr[i]);
                }
                else{
                    if(arr[i].substring(0,2).equals("AD")){
                        if(i==0){
                            list1.clear();
                            continue;
                        }
                        // Character c = arr[i].charAt(3);
                        list1.add("0");
                        list1.add("0");
                        if(i==arr.length-1){
                            list1.add("0");
                        }
                    }
                    else if(arr[i].substring(0,2).equals("IS")){
                        Character c = arr[i].charAt(3);
                        list1.add(c.toString());
                    }
                    else if(arr[i].substring(0,2).equals("DL")){
                        if(arr[i].charAt(3)=='1'){
                            list1.add("0");
                            list1.add("0");
                            list1.add(arr[i+1].split(",")[1]);
                        } else {
                            list1.clear();
                        }
                        break;
                    }
                    else if(arr[i].substring(0,2).equals("DS")){
                        list1.clear();
                        continue;
                        // Character c = arr[i].charAt(3);
                        // list1.add(c.toString());
                    }
                    else if(arr[i].substring(0,1).equals("L")){
                        try {

                            File littab = new File("littab.txt");
                            Scanner lt = new Scanner(littab);
                            Character d = arr[i].charAt(2);

                            while(lt.hasNextLine()){
                                String s = lt.nextLine().trim();
                                String[] a = s.split(" ");
                                if(a[0].equals(d.toString())){
                                    list1.add(a[2]);
                                }
                            }
                            lt.close();
                        } catch (FileNotFoundException e) {
                            System.out.println("No Such File "+e.getMessage());
                        }
                    }
                    else if(arr[i].substring(0,1).equals("S")){
                        try{

                            File symbol = new File("symbol.txt");
                            Scanner st = new Scanner(symbol);
                            Character d = arr[i].charAt(2);
                            while(st.hasNextLine()){
                                String s = st.nextLine().trim();
                                String[] a = s.split(" ");
                                if(a[0].equals(d.toString())){
                                    list1.add(a[2]);
                                }
                            }
                            st.close();
                        }
                        catch(FileNotFoundException e){
                            System.out.println("No Such File "+e.getMessage());
                        }
                    }
                }
            }
            if(list1.size()!=0){
                list.add(list1);
            }
        }
        System.out.println("Machine Code:");
        for (List<String> row : list) {
            for (String value : row) {
            System.out.print(value + " ");
            }
            System.out.println();
        }
    }
    public static void main(String[] args) {
        try{
            File file1 = new File("file1.txt");
            Scanner sc = new Scanner(file1);
            machinecode(sc);
            sc.close();
        }
        catch(FileNotFoundException e){
            System.out.println("No Such File "+e.getMessage());
        }
    }
}
