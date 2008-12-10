Darius’s notes on spell-checking
================================

Options:

1.  hack it. We only have to go up to distance 2.
2.  use only R ops, but keep track of prior deletions and allow free
    insertions where those are equivalent to a prior transposition.
3.  Develop a “patch theory”: a set of edit ops that can be commuted.
    That is, for ops P, Q, with total cost c, where i < j, there’s
    another op composition R S ... T<sub>i</sub>, with R S ... not to
    the left of i, and total cost ≤c.  And all ops T<sub>i</sub> touch
    nothing to the left of position i.  (Our R<sub>slc</sub> ops by
    themselves work.)

    Our R<sub>slc</sub> ops together with rotate ops almost work.  Maybe
    rotate-with-optional-delete?

    Haven’t checked substitute of ... (*unreadable due to covering paper*)

4.  fetch candidates with n-grams in common with the word, then filter
    them by edit distance.  Oh, c’mon.

5.  Allow the search to go back leftwards a bit after a delete?

A patch theory
--------------

<pre>
insert c    I<sub>ic</sub>
replace c   R<sub>ic</sub>
delete      D<sub>i</sub>
transpose   T<sub>i</sub>

D<sub>i</sub> D<sub>j</sub> = D<sub>j+1</sub> D<sub>i</sub> if i ≤ j
T<sub>i</sub> T<sub>i</sub> = 1
</pre>

    n v i d i a
      x
      n i d i a
     ^_/
      i n d i a

    a b c d
         *
        d c
       *
      d b


Let’s introduce an R operation, a generalization of
replace/insert/delete.

<pre>
R<sub>slc</sub> t = t except t[s:s+l] := c
           (where c is a string)
           (|c| ≤ 1)
           0 ≤ l ≤ 1
</pre>

Now consider R<sub>s'l'c'</sub>    R<sub>slc</sub>    t where s' < s  
it’s = to    R<sub>s''l''c''</sub> R<sub>s'l'c'</sub> t for some s'', l'', c'' — right?

So: R's can be commuted among each other.
    Rotates can be commuted among each other. (I think.)
    What about combinations of R's and rotates?
    Two new possibilities:

- a rotate followed by an R to its left:

        a b c d             a b c d |  a b c d
         ^___/               ^___/  | ^_/
        a d b c             a d b c |  b a c d
                           ^___/    |     ^_/
                            b a d c |  b a d c
                            ------------------
                            a b c d | a b c d
                              x     | x x
                              a c d |     c d
                             ^_/    |      ^
                              c a d |   c a d

- an R followed by a rotate to its left.  Deletes:

        a b c d |  a b c d
          x     | ^___/
          a c d |  c a b d
         ^_/    |      x
          c a d |  c a d

    Problem: costs are not equal!
    A deletion in the rotated over should be fine, I guess.

    Inserts:

          a b c d | a b c d
           ^      |    ^
        a e b c d | a b e c d
         ^_/      |
        a b e c d |

          a b c d |  a b c d
           ^      | ^
        a e b c d |  e a b c d
         ^_/      |
        e a b c d |
