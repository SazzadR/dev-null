#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Node {
    int value;
    struct Node *next;
};

struct LinkedList {
    struct Node *head;
};

void print_linked_list(struct LinkedList *list);

int main()
{
    int n = 5;
    int i = 0;

    struct LinkedList list;
    list.head = NULL;

    struct Node *current = NULL;

    while (i < n) {
        struct Node *node = malloc(sizeof(struct Node));
        if (node == NULL) {
            return 1;
        }

        (*node).value = i;
        (*node).next = NULL;

        if (list.head == NULL) {
            list.head = node;
        } else {
            (*current).next = node;
        }

        current = node;

        i++;
    }

    print_linked_list(&list);

    return 0;
}

void print_linked_list(struct LinkedList *list)
{
    struct Node *current = (*list).head;

    while (current != NULL) {
        printf("[%d]->", (*current).value);

        current = (*current).next;
    }
    printf("NULL\n");
}
