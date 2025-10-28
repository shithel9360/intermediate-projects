/**
 * Stack and Queue Implementation in C++
 * 
 * Demonstrates fundamental data structures with detailed explanations:
 * - Stack: Last-In-First-Out (LIFO) structure
 * - Queue: First-In-First-Out (FIFO) structure
 * - Dynamic memory allocation
 * - Template-based implementation for type flexibility
 * - Error handling and edge cases
 * 
 * Author: Intermediate Projects Collection
 */

#include <iostream>
#include <stdexcept>
#include <string>

using namespace std;

// ============================================================================
// STACK IMPLEMENTATION (LIFO - Last In, First Out)
// ============================================================================

/**
 * Template-based Stack class using dynamic arrays
 * Supports any data type (int, string, custom objects, etc.)
 */
template <typename T>
class Stack {
private:
    T* arr;              // Dynamic array to store elements
    int topIndex;        // Index of top element (-1 if empty)
    int capacity;        // Maximum capacity of stack
    
    /**
     * Resize the stack when capacity is reached
     * Doubles the capacity and copies existing elements
     */
    void resize() {
        capacity *= 2;
        T* newArr = new T[capacity];
        
        // Copy existing elements to new array
        for (int i = 0; i <= topIndex; i++) {
            newArr[i] = arr[i];
        }
        
        delete[] arr;  // Free old memory
        arr = newArr;
        cout << "Stack resized to capacity: " << capacity << endl;
    }
    
public:
    /**
     * Constructor: Initialize empty stack with given capacity
     */
    Stack(int size = 10) {
        arr = new T[size];
        capacity = size;
        topIndex = -1;  // Empty stack
        cout << "Stack created with capacity: " << capacity << endl;
    }
    
    /**
     * Destructor: Clean up dynamic memory
     */
    ~Stack() {
        delete[] arr;
        cout << "Stack destroyed" << endl;
    }
    
    /**
     * Push: Add element to top of stack
     * Time Complexity: O(1) amortized
     */
    void push(T value) {
        if (topIndex == capacity - 1) {
            resize();  // Expand if full
        }
        arr[++topIndex] = value;
        cout << "Pushed: " << value << endl;
    }
    
    /**
     * Pop: Remove and return top element
     * Time Complexity: O(1)
     */
    T pop() {
        if (isEmpty()) {
            throw runtime_error("Stack Underflow: Cannot pop from empty stack");
        }
        T value = arr[topIndex--];
        cout << "Popped: " << value << endl;
        return value;
    }
    
    /**
     * Peek: View top element without removing
     * Time Complexity: O(1)
     */
    T peek() const {
        if (isEmpty()) {
            throw runtime_error("Stack is empty: Cannot peek");
        }
        return arr[topIndex];
    }
    
    /**
     * Check if stack is empty
     */
    bool isEmpty() const {
        return topIndex == -1;
    }
    
    /**
     * Get current size of stack
     */
    int size() const {
        return topIndex + 1;
    }
    
    /**
     * Display all elements (top to bottom)
     */
    void display() const {
        if (isEmpty()) {
            cout << "Stack is empty" << endl;
            return;
        }
        cout << "Stack (top to bottom): ";
        for (int i = topIndex; i >= 0; i--) {
            cout << arr[i];
            if (i > 0) cout << " <- ";
        }
        cout << endl;
    }
};

// ============================================================================
// QUEUE IMPLEMENTATION (FIFO - First In, First Out)
// ============================================================================

/**
 * Node structure for linked-list based queue
 */
template <typename T>
struct Node {
    T data;
    Node* next;
    
    Node(T value) : data(value), next(nullptr) {}
};

/**
 * Template-based Queue class using linked list
 * Avoids the circular array complexity
 */
template <typename T>
class Queue {
private:
    Node<T>* frontPtr;   // Points to front of queue
    Node<T>* rearPtr;    // Points to rear of queue
    int count;           // Number of elements
    
public:
    /**
     * Constructor: Initialize empty queue
     */
    Queue() {
        frontPtr = nullptr;
        rearPtr = nullptr;
        count = 0;
        cout << "Queue created" << endl;
    }
    
    /**
     * Destructor: Free all nodes
     */
    ~Queue() {
        while (!isEmpty()) {
            dequeue();
        }
        cout << "Queue destroyed" << endl;
    }
    
    /**
     * Enqueue: Add element to rear of queue
     * Time Complexity: O(1)
     */
    void enqueue(T value) {
        Node<T>* newNode = new Node<T>(value);
        
        if (isEmpty()) {
            // First element
            frontPtr = rearPtr = newNode;
        } else {
            // Add to rear
            rearPtr->next = newNode;
            rearPtr = newNode;
        }
        count++;
        cout << "Enqueued: " << value << endl;
    }
    
    /**
     * Dequeue: Remove and return front element
     * Time Complexity: O(1)
     */
    T dequeue() {
        if (isEmpty()) {
            throw runtime_error("Queue Underflow: Cannot dequeue from empty queue");
        }
        
        Node<T>* temp = frontPtr;
        T value = temp->data;
        frontPtr = frontPtr->next;
        
        // If queue becomes empty
        if (frontPtr == nullptr) {
            rearPtr = nullptr;
        }
        
        delete temp;
        count--;
        cout << "Dequeued: " << value << endl;
        return value;
    }
    
    /**
     * Front: View front element without removing
     * Time Complexity: O(1)
     */
    T front() const {
        if (isEmpty()) {
            throw runtime_error("Queue is empty: Cannot access front");
        }
        return frontPtr->data;
    }
    
    /**
     * Check if queue is empty
     */
    bool isEmpty() const {
        return frontPtr == nullptr;
    }
    
    /**
     * Get current size of queue
     */
    int size() const {
        return count;
    }
    
    /**
     * Display all elements (front to rear)
     */
    void display() const {
        if (isEmpty()) {
            cout << "Queue is empty" << endl;
            return;
        }
        cout << "Queue (front to rear): ";
        Node<T>* current = frontPtr;
        while (current != nullptr) {
            cout << current->data;
            if (current->next != nullptr) cout << " <- ";
            current = current->next;
        }
        cout << endl;
    }
};

// ============================================================================
// DEMONSTRATION AND USE CASES
// ============================================================================

/**
 * Demonstrate stack operations
 */
void demonstrateStack() {
    cout << "\n" << string(80, '=') << endl;
    cout << "STACK DEMONSTRATION (LIFO)" << endl;
    cout << string(80, '=') << "\n" << endl;
    
    Stack<int> intStack(5);
    
    // Push elements
    cout << "\n--- Pushing elements ---" << endl;
    intStack.push(10);
    intStack.push(20);
    intStack.push(30);
    intStack.push(40);
    intStack.push(50);
    intStack.display();
    
    // Peek at top
    cout << "\n--- Peek operation ---" << endl;
    cout << "Top element: " << intStack.peek() << endl;
    
    // Pop elements
    cout << "\n--- Popping elements ---" << endl;
    intStack.pop();
    intStack.pop();
    intStack.display();
    cout << "Current size: " << intStack.size() << endl;
    
    // Test resize
    cout << "\n--- Testing dynamic resize ---" << endl;
    intStack.push(60);
    intStack.push(70);
    intStack.push(80);  // This should trigger resize
    intStack.display();
    
    // String stack example
    cout << "\n--- String Stack Example ---" << endl;
    Stack<string> strStack(3);
    strStack.push("Hello");
    strStack.push("World");
    strStack.push("!");
    strStack.display();
}

/**
 * Demonstrate queue operations
 */
void demonstrateQueue() {
    cout << "\n" << string(80, '=') << endl;
    cout << "QUEUE DEMONSTRATION (FIFO)" << endl;
    cout << string(80, '=') << "\n" << endl;
    
    Queue<int> intQueue;
    
    // Enqueue elements
    cout << "\n--- Enqueuing elements ---" << endl;
    intQueue.enqueue(100);
    intQueue.enqueue(200);
    intQueue.enqueue(300);
    intQueue.enqueue(400);
    intQueue.display();
    
    // Front element
    cout << "\n--- Front operation ---" << endl;
    cout << "Front element: " << intQueue.front() << endl;
    
    // Dequeue elements
    cout << "\n--- Dequeuing elements ---" << endl;
    intQueue.dequeue();
    intQueue.dequeue();
    intQueue.display();
    cout << "Current size: " << intQueue.size() << endl;
    
    // Add more elements
    cout << "\n--- Adding more elements ---" << endl;
    intQueue.enqueue(500);
    intQueue.enqueue(600);
    intQueue.display();
    
    // String queue example
    cout << "\n--- String Queue Example ---" << endl;
    Queue<string> strQueue;
    strQueue.enqueue("First");
    strQueue.enqueue("Second");
    strQueue.enqueue("Third");
    strQueue.display();
    strQueue.dequeue();
    strQueue.display();
}

/**
 * Demonstrate error handling
 */
void demonstrateErrorHandling() {
    cout << "\n" << string(80, '=') << endl;
    cout << "ERROR HANDLING DEMONSTRATION" << endl;
    cout << string(80, '=') << "\n" << endl;
    
    Stack<int> emptyStack(2);
    Queue<int> emptyQueue;
    
    // Test stack underflow
    cout << "\n--- Testing Stack Underflow ---" << endl;
    try {
        emptyStack.pop();  // Should throw exception
    } catch (const runtime_error& e) {
        cout << "Caught exception: " << e.what() << endl;
    }
    
    // Test queue underflow
    cout << "\n--- Testing Queue Underflow ---" << endl;
    try {
        emptyQueue.dequeue();  // Should throw exception
    } catch (const runtime_error& e) {
        cout << "Caught exception: " << e.what() << endl;
    }
    
    // Test peek on empty stack
    cout << "\n--- Testing Peek on Empty Stack ---" << endl;
    try {
        emptyStack.peek();  // Should throw exception
    } catch (const runtime_error& e) {
        cout << "Caught exception: " << e.what() << endl;
    }
}

/**
 * Main function: Run all demonstrations
 */
int main() {
    cout << "\n" << string(80, '=') << endl;
    cout << "DATA STRUCTURES: STACK AND QUEUE IMPLEMENTATION" << endl;
    cout << string(80, '=') << endl;
    
    demonstrateStack();
    demonstrateQueue();
    demonstrateErrorHandling();
    
    cout << "\n" << string(80, '=') << endl;
    cout << "DEMONSTRATION COMPLETED" << endl;
    cout << string(80, '=') << "\n" << endl;
    
    return 0;
}

/**
 * PRACTICAL USE CASES:
 * 
 * Stack Applications:
 * - Function call stack in programming languages
 * - Undo/Redo functionality in text editors
 * - Expression evaluation (postfix/infix conversion)
 * - Backtracking algorithms (maze solving, N-Queens)
 * - Browser back button history
 * 
 * Queue Applications:
 * - Print job scheduling
 * - CPU task scheduling
 * - Breadth-First Search (BFS) in graphs
 * - Message queuing systems
 * - Handling requests in web servers
 */
