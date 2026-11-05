// Task_01
import java.util.ArrayList;
import java.util.List;

class Bank {
    private String name;
    private List<Client> clients = new ArrayList<>();
    private List<Account> accounts = new ArrayList<>();

    public Bank(String name) {
        this.name = name;
    }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public List<Client> getClList() { return clients; }
    public void setClList(List<Client> clList) {
        this.clients = (clList != null) ? clList : new ArrayList<>();
    }

    public List<Account> getAcList() { return accounts; }
    public void setAcList(List<Account> acList) {
        this.accounts = (acList != null) ? acList : new ArrayList<>();
    }

    // Registers a new client from a Person; if that CNIC is already a client, returns the existing one
    public Client addClient(Person p) {
        if (p == null) {
            System.out.println("Person cannot be null.");
            return null;
        }
        Client existing = searchCustomerDetail(p.getCnic());
        if (existing != null) {
            System.out.println("Client with CNIC " + p.getCnic() + " already exists in " + name + ".");
            return existing;
        }
        Client c = new Client(p);
        clients.add(c);
        return c;
    }

    // Registers an existing client (e.g. one who also banks elsewhere)
    public Client addClient(Client c) {
        if (c != null && !clients.contains(c)) {
            clients.add(c);
        }
        return c;
    }

    public Account addAccount(String id, float amount, Client c) {
        if (c == null) {
            System.out.println("Client cannot be null.");
            return null;
        }
        if (searchAccount(id) != null) {
            System.out.println("Account " + id + " already exists in " + name + ".");
            return null;
        }
        addClient(c);
        Account a = new Account(id, amount, c);
        accounts.add(a);
        c.addAccount(a);
        return a;
    }

    public Account searchAccount(String id) {
        for (Account a : accounts) {
            if (id != null && id.equals(a.getNumber())) return a;
        }
        return null;
    }

    public boolean removeClient(String id) {
        Client target = null;
        for (Client c : clients) {
            if (c.getId().equals(id)) { target = c; break; }
        }
        if (target == null) return false;

        List<Account> toRemove = new ArrayList<>();
        for (Account a : accounts) {
            if (a.getACholder() == target) toRemove.add(a);
        }
        accounts.removeAll(toRemove);
        target.getAcList().removeAll(toRemove);
        clients.remove(target);
        return true;
    }

    public float totalAmount() {
        float total = 0;
        for (Account a : accounts) {
            total += a.getAmount();
        }
        return total;
    }

    public Client searchCustomerDetail(String cnic) {
        for (Client c : clients) {
            Person p = c.getPersonDetails();
            if (p != null && cnic != null && cnic.equals(p.getCnic())) return c;
        }
        return null;
    }

    @Override
    public String toString() {
        return "Bank: " + name + " | Clients: " + clients.size()
                + " | Accounts: " + accounts.size() + " | Total: " + totalAmount();
    }
}
