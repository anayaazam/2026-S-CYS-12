// Task_04
class Person {
    private String name;
    private String cnic;
    private String phoneNo;

    public Person() {
        this("", "", "");
    }

    public Person(String name, String cnic, String phoneNo) {
        this.name = name;
        this.cnic = cnic;
        this.phoneNo = phoneNo;
    }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getCnic() { return cnic; }
    public void setCnic(String cnic) { this.cnic = cnic; }

    public String getPhoneNo() { return phoneNo; }
    public void setPhoneNo(String phoneNo) { this.phoneNo = phoneNo; }

    @Override
    public String toString() {
        return "Name: " + name + ", CNIC: " + cnic + ", Phone: " + phoneNo;
    }
}
