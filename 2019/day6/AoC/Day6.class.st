Class {
	#name : #Day6,
	#superclass : #Object,
	#category : #AoC
}

{ #category : #operation }
Day6 >> count: inputString [
	| solarSystem |
	solarSystem := SolarSystem with: inputString.
	^ self countrec: (solarSystem planets) for: 'COM' atDepth: 0.

]

{ #category : #operation }
Day6 >> countTransfers: inputString [ 
	| solarSystem planets santa you tmp |
	solarSystem := SolarSystem with: inputString reverse: true.
	planets := solarSystem planets.
	santa := OrderedCollection new.
	you := OrderedCollection new.
	tmp := 'SAN'.
	[ tmp ~= 'COM' ] whileTrue: [
		tmp := planets at: tmp.
		santa add: tmp beforeIndex: 1.
	].
	tmp := 'YOU'.
	[ tmp ~= 'COM' ] whileTrue: [
		tmp := planets at: tmp.
		you add: tmp beforeIndex: 1.
	].
	[ (you at: 1) == (santa at: 1) ] whileTrue: [
		you removeFirst.
		santa removeFirst.
	].
	Transcript show: santa; cr.
	^ (you size) + (santa size) - 2
]

{ #category : #operation }
Day6 >> countrec: planets for: planet atDepth: depth [ 
	^ (planets at: planet
		ifPresent: [ :children |
			| counts |
			counts := children collect: [ :child |
				self countrec: planets for: child atDepth: (depth + 1)
				 ].
			"Transcript show: planet; cr; show: depth; cr; show: (counts sum); cr."
			(counts sum) ]
		ifAbsent: [ 0 ]) + depth
]

{ #category : #operation }
Day6 >> withSdin [
	| file stream |
	file := '/dev/stdin' asFileReference.
	stream := file readStream.
	^ self count: (stream upToEnd)
]
