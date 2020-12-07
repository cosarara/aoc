Class {
	#name : #Day6Test,
	#superclass : #TestCase,
	#category : #'AoC-Tests'
}

{ #category : #tests }
Day6Test >> testBExample [
	| day6 val input |
	day6 := Day6 new.
	input := 'COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN'.
	val := day6 countTransfers: input.
	self assert: val value equals: 4
]

{ #category : #tests }
Day6Test >> testCreatingDay6 [
	"idk"

	| tmp |
	tmp := Day6 new.
	self deny: tmp equals: nil
]

{ #category : #tests }
Day6Test >> testExample [
	"comment stating purpose of instance-side message"

	"scope: class-variables  &  instance-variables"

	| day6 val input |
	day6 := Day6 new.
	input := 'COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L'.
	val := day6 count: input.
	self assert: val value equals: 42
]

{ #category : #tests }
Day6Test >> testExample2 [
	"comment stating purpose of instance-side message"

	"scope: class-variables  &  instance-variables"

	| day6 val input |
	day6 := Day6 new.
	input := 'COM)B
B)C
C)D
'.
	val := day6 count: input.
	self assert: val value equals: 6
]
