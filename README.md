AryanBlock Programming Language
text

╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║     █████╗ ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗           ║
║    ██╔══██╗██╔══██╗╚██╗ ██╔╝██╔══██╗████╗  ██║           ║
║    ███████║██████╔╝ ╚████╔╝ ███████║██╔██╗ ██║           ║
║    ██╔══██║██╔══██╗  ╚██╔╝  ██╔══██║██║╚██╗██║           ║
║    ██║  ██║██║  ██║   ██║   ██║  ██║██║ ╚████║           ║
║    ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝           ║
║                                                           ║
║    ██████╗ ██╗      ██████╗  ██████╗██╗  ██╗             ║
║    ██╔══██╗██║     ██╔═══██╗██╔════╝██║ ██╔╝             ║
║    ██████╔╝██║     ██║   ██║██║     █████╔╝              ║
║    ██╔══██╗██║     ██║   ██║██║     ██╔═██╗              ║
║    ██████╔╝███████╗╚██████╔╝╚██████╗██║  ██╗             ║
║    ╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝             ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
AryanBlock is a modern, easy-to-learn programming language with clean syntax inspired by Python and Rust.

 Quick Start (5 Minutes)
1. Install
Bash

# Clone or download this repository
git clone https://github.com/yourusername/aryanblock.git
cd aryanblock

# Make sure you have Python 3.8+ installed
python --version
That's it! No dependencies needed.

2. Run Your First Program
Create a file called hello.ab:

JavaScript

start {
    print("Hello, AryanBlock!")
}
Run it:

Bash

python src/main.py run hello.ab
Output:

text

Hello, AryanBlock!
3. Try the Interactive REPL
Bash

python src/main.py repl
You'll see:

text

╔═══════════════════════════════════════════════════════════╗
║     AryanBlock v1.0.0                                     ║
║     Type :help for commands, :quit to exit                ║
╚═══════════════════════════════════════════════════════════╝

ab> 
Try typing:

JavaScript

ab> print("Hello!")
Hello!

ab> 5 + 10
→ 15

ab> let name = "Aryan"
ab> print("Hi, ${name}!")
Hi, Aryan!

ab> :quit
★ Goodbye! ★
📖 Learn AryanBlock in 10 Minutes
Variables
JavaScript

// Immutable (can't change)
let name = "Aryan"

// Mutable (can change)
mut score = 100
score = 150  // OK

// Constant
const PI = 3.14159

// With type annotation
let age: int = 25
Data Types
JavaScript

// Numbers
let x = 42           // integer
let y = 3.14         // float

// Strings
let greeting = "Hello"
let message = "Hi, ${name}!"  // string interpolation

// Booleans
let isActive = true

// Arrays
let numbers = [1, 2, 3, 4, 5]

// Maps (dictionaries)
let person = {
    "name": "Aryan",
    "age": 25
}

// Null
let nothing = null
Math Operations
JavaScript

let a = 10
let b = 3

print(a + b)   // 13 (addition)
print(a - b)   // 7  (subtraction)
print(a * b)   // 30 (multiplication)
print(a / b)   // 3.333... (division)
print(a % b)   // 1  (modulo/remainder)
print(a ** b)  // 1000 (power: 10^3)
If/Else
JavaScript

let score = 85

if score >= 90 {
    print("Grade: A")
} elif score >= 80 {
    print("Grade: B")
} elif score >= 70 {
    print("Grade: C")
} else {
    print("Grade: F")
}
Loops
JavaScript

// Loop 5 times
loop 5 {
    print("Hello!")
}

// For loop with range
for i in 0..10 {
    print(i)  // prints 0 to 9
}

// For each loop
let fruits = ["apple", "banana", "orange"]
for fruit in fruits {
    print(fruit)
}

// While loop
mut count = 0
while count < 5 {
    print(count)
    count += 1
}
Functions
JavaScript

// Basic function
func greet(name: string) {
    print("Hello, ${name}!")
}

greet("Aryan")  // Hello, Aryan!

// Function with return value
func add(a: int, b: int) -> int {
    return a + b
}

let result = add(5, 3)
print(result)  // 8

// Default parameters
func connect(host: string, port: int = 8080) {
    print("Connecting to ${host}:${port}")
}

connect("localhost")          // uses port 8080
connect("example.com", 3000)  // uses port 3000

// Lambda (anonymous function)
let double = (x) => x * 2
print(double(5))  // 10
Classes
JavaScript

class Person {
    let name: string
    mut age: int
    
    // Constructor
    init(name: string, age: int) {
        self.name = name
        self.age = age
    }
    
    // Method
    func greet() {
        print("Hi, I'm ${self.name}, ${self.age} years old")
    }
    
    func birthday() {
        self.age += 1
        print("Happy birthday! Now ${self.age}")
    }
}

// Create an object
let person = Person("Aryan", 25)
person.greet()      // Hi, I'm Aryan, 25 years old
person.birthday()   // Happy birthday! Now 26
Blocks (Namespaces)
JavaScript

block MathUtils {
    func square(n: int) -> int {
        return n * n
    }
    
    func cube(n: int) -> int {
        return n * n * n
    }
}

// Use the block
print(MathUtils.square(5))  // 25
print(MathUtils.cube(3))    // 27
User Input
JavaScript

let name = input("What's your name? ")
print("Hello, ${name}!")

let age = int(input("How old are you? "))
print("You are ${age} years old")
Match (Switch)
JavaScript

let day = 3

match day {
    1 => print("Monday"),
    2 => print("Tuesday"),
    3 => print("Wednesday"),
    4 => print("Thursday"),
    5 => print("Friday"),
    _ => print("Weekend!")
}
🎮 REPL Commands
When you run python src/main.py repl, you can use these commands:

Command	What it does	Example
:help	Show help	:help
:quit	Exit REPL	:quit
:clear	Clear screen	:clear
:reset	Reset all variables	:reset
:env	Show current variables	:env
:load <file>	Run a .ab file	:load hello.ab
:pwd	Show current folder	:pwd
:ls	List .ab files	:ls
📚 Built-in Functions
Input/Output
JavaScript

print("Hello")              // Print to console
let name = input("Name: ")  // Get user input
Math
JavaScript

abs(-5)           // 5 (absolute value)
min(1, 2, 3)      // 1
max(1, 2, 3)      // 3
sum([1, 2, 3])    // 6
sqrt(16)          // 4.0 (square root)
pow(2, 3)         // 8 (2^3)
floor(3.7)        // 3
ceil(3.2)         // 4
round(3.5)        // 4
random()          // Random 0.0-1.0
random_int(1, 10) // Random integer 1-10
Type Conversion
JavaScript

int("42")      // 42
float("3.14")  // 3.14
str(100)       // "100"
bool(1)        // true
Arrays
JavaScript

let arr = [1, 2, 3]

len(arr)              // 3 (length)
push(arr, 4)          // [1, 2, 3, 4]
pop(arr)              // removes last item
reverse(arr)          // [3, 2, 1]
sort(arr)             // sorted
contains(arr, 2)      // true
join(arr, ", ")       // "1, 2, 3"
Strings
JavaScript

let text = "Hello"

len(text)                    // 5
upper(text)                  // "HELLO"
lower(text)                  // "hello"
trim("  hi  ")               // "hi"
replace(text, "H", "J")      // "Jello"
split("a,b,c", ",")          // ["a", "b", "c"]
contains(text, "ell")        // true
💡 Example Programs
1. Calculator
JavaScript

start {
    let a = float(input("First number: "))
    let op = input("Operation (+, -, *, /): ")
    let b = float(input("Second number: "))
    
    mut result = 0.0
    
    match op {
        "+" => result = a + b,
        "-" => result = a - b,
        "*" => result = a * b,
        "/" => result = a / b,
        _ => print("Unknown operation!")
    }
    
    print("${a} ${op} ${b} = ${result}")
}
2. Fibonacci
JavaScript

func fib(n: int) -> int {
    if n <= 1 {
        return n
    }
    
    mut a = 0
    mut b = 1
    
    for i in 2..n+1 {
        let temp = a + b
        a = b
        b = temp
    }
    
    return b
}

start {
    for i in 0..10 {
        print("fib(${i}) = ${fib(i)}")
    }
}
3. Guessing Game
JavaScript

start {
    print("I'm thinking of a number between 1 and 100")
    
    let secret = random_int(1, 100)
    mut attempts = 0
    mut guessed = false
    
    while not guessed {
        let guess = int(input("Your guess: "))
        attempts += 1
        
        if guess == secret {
            print("Correct! It took you ${attempts} tries!")
            guessed = true
        } elif guess < secret {
            print("Too low!")
        } else {
            print("Too high!")
        }
    }
}
📁 File Structure
When you create a program, save it with the .ab extension:

text

my_project/
├── main.ab          ← Your main program
├── utils.ab         ← Utility functions
└── game.ab          ← Game logic
Run with:

Bash

python src/main.py run my_project/main.ab
🔧 Common Tasks
Print multiple values
JavaScript

print("Name:", name, "Age:", age)
Get array length
JavaScript

let count = len(myArray)
Convert string to number
JavaScript

let num = int("42")
let decimal = float("3.14")
Check if value exists
JavaScript

if contains(myArray, 5) {
    print("Found 5!")
}
Loop with index
JavaScript

for i in 0..len(items) {
    print("${i}: ${items[i]}")
}
❓ FAQ
Q: Do I need to install anything?
A: Just Python 3.8 or newer. That's it!

Q: How do I run a program?
A: python src/main.py run yourfile.ab

Q: How do I exit the REPL?
A: Type :quit or press Ctrl+D

Q: Can I use AryanBlock for real projects?
A: It's a learning/hobby language. Great for learning programming concepts!

Q: Why does it say "ab: command not found"?
A: Run it with python src/main.py instead, or install it globally with pip install -e .

Q: How do I report bugs?
A: Open an issue on GitHub!

🎯 Next Steps
✅ Try the examples in the examples/ folder:

Bash

python src/main.py run examples/hello.ab
python src/main.py run examples/calculator.ab
python src/main.py run examples/fibonacci.ab
✅ Experiment in the REPL:

Bash

python src/main.py repl
✅ Create your own program:

Make a new .ab file
Start with start { ... }
Run it!
✅ Learn more:

Check examples/ for more complex programs
Try creating classes and functions
Build something fun!
📄 License
MIT License - Use it however you want!

👨‍💻 Author
Created with ❤️ by Aryan

🌟 Have Fun!
AryanBlock is designed to be easy and fun. If you get stuck:

Try the examples
Use the REPL to experiment
Read the error messages (they try to be helpful!)
Check this README again
Happy coding! 🚀

Quick Reference Card
text

╔════════════════════════════════════════════════════════╗
║  ARYANBLOCK QUICK REFERENCE                            ║
╠════════════════════════════════════════════════════════╣
║  Variables:                                            ║
║    let x = 10          (immutable)                     ║
║    mut y = 20          (mutable)                       ║
║                                                        ║
║  Control Flow:                                         ║
║    if condition { }                                    ║
║    for i in 0..10 { }                                  ║
║    while condition { }                                 ║
║    loop 5 { }                                          ║
║                                                        ║
║  Functions:                                            ║
║    func name(param: type) -> type { }                  ║
║                                                        ║
║  Classes:                                              ║
║    class Name {                                        ║
║      init(params) { }                                  ║
║      func method() { }                                 ║
║    }                                                   ║
║                                                        ║
║  Run Program:                                          ║
║    python src/main.py run file.ab                      ║
║                                                        ║
║  Start REPL:                                           ║
║    python src/main.py repl                             ║
╚════════════════════════════════════════════════════════╝
