-- Naïve implementation where we note
-- all the points passed on the first cable,
-- then check for them on the second cable (point by point)
--
-- A much better algorithm would note only the start and end of each line
-- then check for intersections
--
-- https://learn.adacore.com/courses/intro-to-ada/chapters/subprograms.html
with Ada.Text_IO; use Ada.Text_IO;
with Ada.Containers.Indefinite_Vectors; use Ada.Containers;
with Ada.Integer_Text_IO; use Ada.Integer_Text_IO;
with Ada.Strings; use Ada.Strings;
with Ada.Strings.Fixed; use Ada.Strings.Fixed;
-- with Ada.Strings.Unbounded; use Ada.Strings.Unbounded;

procedure Day3 is

    package SV is new Indefinite_Vectors (Natural,String);

    type Point is
        record
            X : Integer;
            Y : Integer;
        end record;

    package PV is new Indefinite_Vectors (Natural,Point);

    -- thanks rosetta code
    function split (s: String) return SV.Vector is
        current : Positive := s'First;
        v : SV.Vector;
        c : Character;
    begin
        for i in s'range loop
            c := s (i);
            if c = ',' then
                v.append (s (current .. i-1));
                current := i + 1;
            elsif i = s'last then
                v.append (s (current .. i));
            end if;
        end loop;
        return v;
    end Split;

begin
    Put_Line ("hi day 3");
    declare
        CableA : SV.Vector := Split(Get_Line);
        CableB : SV.Vector := Split(Get_Line);
        P : Point := (X => 0, Y => 0);
        Best : Point := (X => 0, Y=> 0);
        Passed : PV.Vector;

    begin
        Put_Line("Processing 1st path");

        for Item of CableA loop
            declare
                Direction : Character := Item (Item'first);
                SLength : String := Item (Item'first + 1 .. Item'last);
                Length : Natural := Natural'Value(SLength);
            begin
                -- Put_Line("Item: " & Item);
                -- Put_Line(SLength);
                for i in Integer range 1..Length loop
                    case Direction is
                        when 'R' =>
                            P.X := P.X + 1;
                        when 'L' =>
                            P.X := P.X - 1;
                        when 'U' =>
                            P.Y := P.Y + 1;
                        when 'D' =>
                            P.Y := P.Y - 1;
                        when others =>
                            Put_Line("bad direction " & Direction);
                            null; -- todo exit
                    end case;
                    Passed.append(P);
                end loop;
            end;

            --Put_Line(Item (Item'first..Item'first));
            --Put_Line(Item (Item'first + 1 .. Item'last));
        end loop;

        P := (X => 0, Y => 0);

        Put_Line("Nodes: " & Passed.Length'Image);

        Put_Line("Processing 2nd path");
        -- ok this is terribly inelegant now
        for Item of CableB loop
            declare
                Direction : Character := Item (Item'first);
                SLength : String := Item (Item'first + 1 .. Item'last);
                Length : Natural := Natural'Value(SLength);
            begin
                Put_Line("Item: " & Item);
                -- Put_Line(SLength);
                for i in Integer range 1..Length loop
                    case Direction is
                        when 'R' =>
                            P.X := P.X + 1;
                        when 'L' =>
                            P.X := P.X - 1;
                        when 'U' =>
                            P.Y := P.Y + 1;
                        when 'D' =>
                            P.Y := P.Y - 1;
                        when others =>
                            Put_Line("bad direction " & Direction);
                            null; -- todo exit
                    end case;

                    -- find in passed
                    for Q of Passed loop
                        if P = Q then
                            Put_Line("Intersection!");
                            Put_Line("P: " & P.X'Image & ", " & P.Y'Image);
                            Put_Line("Q: " & Q.X'Image & ", " & Q.Y'Image);
                            if (Best.X = 0 and Best.Y = 0) or abs(Best.X) + abs(Best.Y) > abs(P.X) + abs(P.Y) then
                                Best := P;
                            end if;
                        end if;
                    end loop;
                end loop;
            end;

        end loop;
        Put_Line("Closest point: " & Best.X'Image & ", " & Best.Y'Image);
    end;
end Day3;
