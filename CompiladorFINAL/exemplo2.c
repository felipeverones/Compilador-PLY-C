int main() {

    int age = 6;
    int level = 0;

    if (age < 18) {
	level = 1;
    } else {
	if (age <= 60) {
	   level = 2;
    	} else {
	   level = 3;
    	}
    }
}