// pyramid.cpp
//
// g++ -g pyramid.cpp -o pyramid
#include <stdio.h>
#include <iostream>
#include <iomanip>
#include <string>
#include <stdlib.h>
#include <time.h>
#include <string.h>

enum directions { down, up, left, right };

class tri
{
public:
    tri()
        {
            parent = child = left = right = NULL;
            state = unfilled;
            id = ++next_id;
            dir = up;
        }
    tri(tri& other);
    void dump(int indent = 0);

    enum states { unfilled, filled, frozen };

    static int next_id;

    tri *parent, *child, *left, *right;
    directions dir;
    int id;
    states state;
};

int tri::next_id = 0;

tri::tri(tri& other)
{
    parent = child = left = right = NULL;
    state = other.state;
    id = other.id;
}

void
tri::dump(int indent)
{
    if (indent)
        std::cout << std::string(indent * 2, ' ');

    switch(state)
    {
        case unfilled:
            std::cout << std::setw(2) << " .";
        break;
        case filled:
            std::cout << std::setw(2) << " X";
        break;
        case frozen:
            std::cout << std::setw(2) << " |";
        break;
    }
}

class pyramid
{
public:
    pyramid(int size);
    int add(unsigned int row_idx, unsigned int node_idx, unsigned int size = 2);
    int add(tri *node, int size, directions dir);
    void try_to_freeze(tri *node);
    void dump();
    void clear(tri *node);
    void freeze(tri *node);
    void count();
    tri *top;
    int row_cnt;
    int *horiz_cnt;
    int *north_west_cnt;
    int *north_east_cnt;
};

void
pyramid::clear(tri *node)
{
    tri *start = node;
    while(node)
    {
        node->state = tri::unfilled;
        node = node->right;
    }
    if (start->child)
        this->clear(start->child->left);
    memset(horiz_cnt, 0, row_cnt);
    memset(north_west_cnt, 0, row_cnt);
    memset(north_east_cnt, 0, row_cnt);
}

void
pyramid::try_to_freeze(tri *node)
{
    if (node && node->state == tri::unfilled)
        node->state = tri::frozen;
}

// count the number of filled triangles in each row and column
void
pyramid::count()
{
    tri *node, *start;
    start = node = top;
    int row_idx = 0;

    // the rows
    while(1)
    {
        if (node->state == tri::filled)
            horiz_cnt[row_idx]++;

        if (node->right) {
            node = node->right;
            continue;
        }
        if (start->child) {
            start = node = start->child->left;
            horiz_cnt[++row_idx] = 0;
            continue;
        }
        break;
    }

    // the columns running northwest and southeast
    row_idx = 0;
    start = node = top;
    directions dir = down;
    while(1)
    {
        if (node->state == tri::filled)
            north_west_cnt[row_idx]++;

        if (dir == down && node->child)
        {
            node = node->child;
            dir = right;
            continue;
        }

        if (dir == right && node->right)
        {
            node = node->right;
            dir = down;
            continue;
        }
        
        if (start->child && start->child->left)
        {
            start = node = start->child->left;
            north_west_cnt[++row_idx] = 0;
            continue;
        }
        break;
    }

    // the columns running northeast and southwest
    row_idx = 0;
    start = node = top;
    dir = down;
    while(1)
    {
        if (node->state == tri::filled)
            north_east_cnt[row_idx]++;

        if (dir == down && node->child)
        {
            node = node->child;
            dir = left;
            continue;
        }

        if (dir == left && node->left)
        {
            node = node->left;
            dir = down;
            continue;
        }

        if (start->child && start->child->right)
        {
            start = node = start->child->right;
            north_east_cnt[++row_idx] = 0;
            continue;
        }

        break;
    }
}

void
pyramid::freeze(tri *node)
{
    tri *start = node;
    while(node)
    {
        if (node->state == tri::filled)
        {
            if (node->left)
            {
                try_to_freeze(node->left);
                try_to_freeze(node->left->parent);
                try_to_freeze(node->left->child);
                if (node->left->left)
                {
                    try_to_freeze(node->left->left);
                    if (node->dir == down)
                        try_to_freeze(node->left->left->parent);
                    else
                        try_to_freeze(node->left->left->child);
                }
            }
            if (node->right)
            {
                try_to_freeze(node->right);
                try_to_freeze(node->right->parent);
                try_to_freeze(node->right->child);
                if (node->right->right)
                {
                    try_to_freeze(node->right->right);
                    if (node->dir == down)
                        try_to_freeze(node->right->right->parent);
                    else
                        try_to_freeze(node->right->right->child);
                }
            }
            if (node->parent)
            {
                try_to_freeze(node->parent);
                try_to_freeze(node->parent->left);
                try_to_freeze(node->parent->right);
            }
            if (node->child)
            {
                try_to_freeze(node->child);
                try_to_freeze(node->child->left);
                try_to_freeze(node->child->right);
            }
        }
        node = node->right;
    }
    if (start->child)
        this->freeze(start->child->left);
}

pyramid::pyramid(int size)
{
    row_cnt = size;
    top = NULL;

    tri *prev_node, *start_of_current_row, *parent_node;
    tri *new_node = top = parent_node = new_node = new tri();

    horiz_cnt = new int[row_cnt];
    north_west_cnt = new int[row_cnt];
    north_east_cnt = new int[row_cnt];

    memset(horiz_cnt, 0, row_cnt);
    memset(north_west_cnt, 0, row_cnt);
    memset(north_east_cnt, 0, row_cnt);

    // create row_cnt rows
    for (int row_idx = 1; row_idx < row_cnt; row_idx++)
    {
        prev_node = NULL;
        int node_cnt = 1 + row_idx * 2;

        // create node_cnt nodes
        for (int node_idx = 0; node_idx < node_cnt; node_idx++)
        {
            new_node = new tri();

            new_node->dir = ((node_idx % 2) ? down : up);

            // save the first node
            if (node_idx == 0)
                start_of_current_row = new_node;

            if (prev_node)
            {
                prev_node->right = new_node;
                new_node->left = prev_node;
            }
            prev_node = new_node;

            if (node_idx > 0 && node_idx < (node_cnt - 1))
            {
                // find a parent for this node
                new_node->parent = parent_node;
                parent_node->child = new_node;
                parent_node = parent_node->right;
            }
        }
        parent_node = start_of_current_row;
    }
}

int
pyramid::add(unsigned int row_idx, unsigned int node_idx, unsigned int size)
{
    tri *node;
    node = top;
    directions dir;

    // std::cout << "row_idx=" << row_idx << ", node_idx=" << node_idx << ", size=" << size << "\n";

    dir = (node_idx % 2) ? up : down;

    while (row_idx && node)
    {
        node = node->child ? node->child->left : NULL;
        row_idx--;
    }

    if (!node)
    {
        std::cerr << "ERROR: row out of range\n";
        return 1;
    }

    while (node_idx && node)
    {
        node = node->right;
        node_idx--;
    }

    if (!node)
    {
        std::cerr << "ERROR: node out of range\n";
        return 1;
    }

    if (add(node, size, dir))
        return 1;

    freeze(top);
    return 0;
}

int
pyramid::add(tri *node, int size, directions dir)
{
    if (!size) return 0;

    if (!node)
    {
        // std::cerr << "ERROR: went over the edge\n";
        return 1;
    }

    if (node->state == tri::frozen)
    {
        // std::cerr << "ERROR: overlap!\n";
        return 1;
    }

    node->state = tri::filled;

    if (size == 1)
        return 0;

    tri *next = (dir == down ? node->child : node->parent);

    if (add(next, size - 1, dir))
        return 1;

    if (add(next->left, size - 1, dir))
        return 1;

    if (add(next->right, size - 1, dir))
        return 1;

    return 0;
}

void
pyramid::dump()
{
    tri *node, *start_of_row;
    node = start_of_row = top;
    int row_idx = 0;
    int indent = row_cnt - 1;

    std::cout << std::string(2 + indent * 2, ' ');
    std::cout << horiz_cnt[row_idx] << " ";
    while (node)
    {
        node->dump();
        node = node->right;
        if (!node)
        {
            std::cout << " " << north_east_cnt[row_idx] << " \n";
            if (start_of_row->child && start_of_row->child->left)
            {
                row_idx++;            
                std::cout << std::string(indent * 2, ' ');
                std::cout << horiz_cnt[row_idx] << " ";
                node = start_of_row = start_of_row->child->left;
            }
            indent = row_cnt - row_idx - 1;
        }
    }

    std::cout << "  ";
    for (row_idx = row_cnt - 1; row_idx >= 0; row_idx--)
    {
        std::cout << std::setw(4) << north_west_cnt[row_idx];
    }
    std::cout << "\n";
}

int
main(int argc, char **argv)
{
    srand(time(NULL));

    int row, col, psize, trisize;

    if (argc > 1)
        psize = atoi(argv[1]);
    else
        psize = 18; // 6 + rand() % 14;
    pyramid p(psize);
    p.add(1, 0, 9);
    // if (p.add(7, 8, 3))
    // return -1;
    // p.clear(p.top);
    // while (p.add(row, col, trisize));

    int tricnt = 0; // (rand() % 3);
    for (int i=0; i<tricnt; i++)
    {
        row = rand() % psize;
        col = rand() % (1 + row * 2);
        trisize = 3; // + (rand() % 3);
        if (p.add(row, col, trisize))
        {
            p.clear(p.top);
            i = 0;
        }
    }
    p.count();
    p.dump();
}
