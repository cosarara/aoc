Class {
	#name : #SolarSystem,
	#superclass : #Object,
	#instVars : [
		'planets'
	],
	#category : #AoC
}

{ #category : #'instance creation' }
SolarSystem class >> with: inputString [
	^ self with: inputString reverse: false
]

{ #category : #'instance creation' }
SolarSystem class >> with: inputString reverse: reverse [
	"comment stating purpose of instance-side message"
	"scope: class-variables  &  instance-variables"	
	| orbits string planets |
	planets := Dictionary new.
	string := inputString.
	string := string copyWithRegex: '\s+$' matchesReplacedWith: ''. "remove trailing whitespace"
	"normalize cr/lf/crlf"
	string := string copyWithRegex: '[',({Character cr . Character lf} as: String),']+'
		matchesReplacedWith: ({Character cr} as: String).
	orbits := string splitOn: Character cr.
	orbits do: [ :orbitString |
		| orbit from to |
		orbit := orbitString splitOn: $).
		from := orbit at: 1.
		to := orbit at: 2.
		reverse
			ifTrue: [
				planets at: to put: from.
			]
			ifFalse: [
				planets at: from ifAbsentPut: (OrderedCollection new).
				(planets at: from) add: to.
			].
		reverse ifTrue: [ orbit := orbit reversed ].
		
		].
	^ self new
		planets: planets.
]

{ #category : #initialization }
SolarSystem >> initialize [
	super.
	planets := Dictionary new.
]

{ #category : #accessing }
SolarSystem >> planets [
	"comment stating purpose of instance-side message"
	"scope: class-variables  &  instance-variables"	
	^ planets
]

{ #category : #accessing }
SolarSystem >> planets: p [
	"this is fucking stupid and this language sucks.
	There is absolutely no reason this attribute has to be public for writing.
	In fact, I don't want it to be.
	But for some reason, I can't write a proper constructor beyond the stupid
	`with:` that, by the way, is hidden between a UI toggle (press Class side)."
	planets := p
]
