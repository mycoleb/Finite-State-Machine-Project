import React, { useState, useEffect } from 'react';

const FSMVisualizer = () => {
  const [fsmType, setFsmType] = useState('dfa');
  const [inputString, setInputString] = useState('');
  const [result, setResult] = useState(null);
  const [currentState, setCurrentState] = useState(null);
  const [processingSteps, setProcessingSteps] = useState([]);
  const [animationFrame, setAnimationFrame] = useState(0);
  const [isAnimating, setIsAnimating] = useState(false);

  // Define FSM configurations
  const dfaConfig = {
    states: ['q0', 'q1', 'q2'],
    alphabet: ['a', 'b', 'c'],
    transitions: {
      'q0': { 'a': 'q1', 'b': 'q1' },
      'q1': { 'c': 'q1' }
    },
    startState: 'q0',
    acceptStates: ['q1'],
    description: 'DFA for language (a+b)c*'
  };

  const nfaConfig = {
    states: ['q0', 'q1', 'q2', 'q3'],
    alphabet: ['a', 'b'],
    transitions: {
      'q0': { 'a': ['q0', 'q1'], 'b': ['q0'] },
      'q1': { 'b': ['q2'] },
      'q2': { 'b': ['q3'] }
    },
    startState: 'q0',
    acceptStates: ['q3'],
    description: 'NFA for language (a|b)*abb'
  };

  // Get the current FSM configuration based on user selection
  const getCurrentFSM = () => (fsmType === 'dfa' ? dfaConfig : nfaConfig);

  // Process the input string
  const processString = (input) => {
    const fsm = getCurrentFSM();
    const steps = [];
    let currentStates = fsmType === 'dfa' ? [fsm.startState] : [fsm.startState];
    steps.push({ symbol: '', states: [...currentStates], accepted: false });

    // Process each character in the input
    for (const symbol of input) {
      if (!fsm.alphabet.includes(symbol)) {
        setResult({ accepted: false, message: `Invalid symbol: ${symbol}` });
        setProcessingSteps(steps);
        return;
      }

      const nextStates = [];
      
      for (const state of currentStates) {
        const transitions = fsm.transitions[state] || {};
        const targets = transitions[symbol] || [];
        
        if (fsmType === 'dfa') {
          if (targets) nextStates.push(targets);
        } else {
          if (Array.isArray(targets)) {
            nextStates.push(...targets);
          }
        }
      }

      currentStates = nextStates;
      const isAccepted = currentStates.some(state => fsm.acceptStates.includes(state));
      steps.push({ symbol, states: [...currentStates], accepted: isAccepted });
      
      if (currentStates.length === 0) {
        break;
      }
    }

    const isAccepted = currentStates.some(state => fsm.acceptStates.includes(state));
    setResult({ 
      accepted: isAccepted, 
      message: isAccepted ? "String accepted" : "String rejected" 
    });
    setProcessingSteps(steps);
    setCurrentState(isAccepted);
  };

  // Handle the test button click
  const handleTest = () => {
    setAnimationFrame(0);
    setIsAnimating(false);
    processString(inputString);
  };

  // Handle animation
  const startAnimation = () => {
    setAnimationFrame(0);
    setIsAnimating(true);
  };

  useEffect(() => {
    if (isAnimating && animationFrame < processingSteps.length) {
      const timer = setTimeout(() => {
        setAnimationFrame(prevFrame => prevFrame + 1);
      }, 1000);
      return () => clearTimeout(timer);
    } else {
      setIsAnimating(false);
    }
  }, [isAnimating, animationFrame, processingSteps.length]);

  // Get a color for the state node based on its status
  const getStateColor = (state, currentStates, isAcceptState) => {
    if (currentStates && currentStates.includes(state)) {
      return result?.accepted ? 'bg-green-500' : 'bg-blue-500';
    }
    return isAcceptState ? 'bg-gray-300 border-2 border-gray-600' : 'bg-gray-200';
  };

  // Render the FSM diagram
  const renderFSMDiagram = () => {
    const fsm = getCurrentFSM();
    const currentFrameData = processingSteps[animationFrame];
    const currentStates = currentFrameData ? currentFrameData.states : [fsm.startState];

    return (
      <div className="relative h-64 bg-white rounded-lg shadow-md p-4 overflow-hidden">
        {/* States */}
        {fsm.states.map((state, index) => {
          const angle = (2 * Math.PI * index) / fsm.states.length;
          const radius = 100;
          const x = radius * Math.cos(angle) + 150;
          const y = radius * Math.sin(angle) + 120;
          const isAcceptState = fsm.acceptStates.includes(state);
          const stateColor = getStateColor(state, currentStates, isAcceptState);

          return (
            <div 
              key={state}
              className={`absolute w-12 h-12 rounded-full flex items-center justify-center ${stateColor} transform -translate-x-1/2 -translate-y-1/2`}
              style={{ left: x, top: y }}
            >
              <div className={isAcceptState ? "w-10 h-10 rounded-full border-2 border-black flex items-center justify-center" : ""}>
                {state}
              </div>
            </div>
          );
        })}

        {/* Transitions */}
        <svg className="absolute top-0 left-0 w-full h-full" style={{ zIndex: -1 }}>
          {fsm.states.map((fromState, fromIndex) => {
            const fromAngle = (2 * Math.PI * fromIndex) / fsm.states.length;
            const fromRadius = 100;
            const fromX = fromRadius * Math.cos(fromAngle) + 150;
            const fromY = fromRadius * Math.sin(fromAngle) + 120;

            const transitions = [];

            Object.entries(fsm.transitions[fromState] || {}).forEach(([symbol, toStates]) => {
              const toStateList = Array.isArray(toStates) ? toStates : [toStates];

              toStateList.forEach(toState => {
                const toIndex = fsm.states.indexOf(toState);
                if (toIndex !== -1) {
                  const toAngle = (2 * Math.PI * toIndex) / fsm.states.length;
                  const toRadius = 100;
                  const toX = toRadius * Math.cos(toAngle) + 150;
                  const toY = toRadius * Math.sin(toAngle) + 120;

                  // Self-loop
                  if (fromState === toState) {
                    const selfLoopRadius = 20;
                    const loopX = fromX + selfLoopRadius * Math.cos(fromAngle - Math.PI / 2);
                    const loopY = fromY + selfLoopRadius * Math.sin(fromAngle - Math.PI / 2);

                    transitions.push(
                      <g key={`${fromState}-${toState}-${symbol}`}>
                        <path
                          d={`M ${fromX} ${fromY} 
                            C ${fromX + 30 * Math.cos(fromAngle - Math.PI / 4)} ${fromY + 30 * Math.sin(fromAngle - Math.PI / 4)}, 
                            ${loopX + 30 * Math.cos(fromAngle + Math.PI / 4)} ${loopY + 30 * Math.sin(fromAngle + Math.PI / 4)}, 
                            ${loopX} ${loopY}`}
                          fill="none"
                          stroke="black"
                          strokeWidth="1.5"
                          markerEnd="url(#arrowhead)"
                        />
                        <text x={loopX + 5} y={loopY - 5} className="text-xs">{symbol}</text>
                      </g>
                    );
                  } else {
                    // Regular transition
                    const midX = (fromX + toX) / 2;
                    const midY = (fromY + toY) / 2;
                    
                    // Add slight curve to the line
                    const dx = toX - fromX;
                    const dy = toY - fromY;
                    const dist = Math.sqrt(dx * dx + dy * dy);
                    const nx = -dy / dist * 15; // Normal vector X component
                    const ny = dx / dist * 15; // Normal vector Y component
                    
                    const ctrlX = midX + nx;
                    const ctrlY = midY + ny;

                    transitions.push(
                      <g key={`${fromState}-${toState}-${symbol}`}>
                        <path
                          d={`M ${fromX} ${fromY} Q ${ctrlX} ${ctrlY} ${toX} ${toY}`}
                          fill="none"
                          stroke={currentFrameData && currentFrameData.symbol === symbol && currentStates.includes(fromState) ? "red" : "black"}
                          strokeWidth={currentFrameData && currentFrameData.symbol === symbol && currentStates.includes(fromState) ? "3" : "1.5"}
                          markerEnd="url(#arrowhead)"
                        />
                        <text x={ctrlX + 5} y={ctrlY - 5} className="text-xs">{symbol}</text>
                      </g>
                    );
                  }
                }
              });
            });

            return transitions;
          })}

          {/* Arrowhead marker definition */}
          <defs>
            <marker
              id="arrowhead"
              viewBox="0 0 10 10"
              refX="8"
              refY="5"
              markerWidth="6"
              markerHeight="6"
              orient="auto-start-reverse"
            >
              <path d="M 0 0 L 10 5 L 0 10 z" fill="black" />
            </marker>
          </defs>
        </svg>

        {/* Start state marker */}
        <div className="absolute w-24 flex justify-center" style={{ top: '50%', left: 0 }}>
          <svg width="30" height="20">
            <path d="M 0 10 L 30 10" stroke="black" strokeWidth="1.5" markerEnd="url(#arrowhead)" />
          </svg>
        </div>
      </div>
    );
  };

  // Example strings
  const exampleStrings = fsmType === 'dfa' 
    ? ['a', 'b', 'ac', 'bc', 'acc', 'bcc', 'c', 'ab', 'ba'] 
    : ['abb', 'aabb', 'babb', 'aaabb', 'ab', 'ba', 'b'];

  return (
    <div className="bg-gray-50 p-4 rounded-lg shadow-lg max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-4 text-center">Finite State Machine Visualizer</h1>
      
      {/* FSM Type Selection */}
      <div className="mb-4 flex justify-center gap-4">
        <button 
          className={`px-4 py-2 rounded-md ${fsmType === 'dfa' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
          onClick={() => setFsmType('dfa')}
        >
          DFA (a+b)c*
        </button>
        <button 
          className={`px-4 py-2 rounded-md ${fsmType === 'nfa' ? 'bg-blue-500 text-white' : 'bg-gray-200'}`}
          onClick={() => setFsmType('nfa')}
        >
          NFA (a|b)*abb
        </button>
      </div>
      
      {/* Description */}
      <div className="mb-4 p-2 bg-blue-50 rounded-md text-center">
        {getCurrentFSM().description}
      </div>
      
      {/* FSM Diagram */}
      <div className="mb-4">
        {renderFSMDiagram()}
      </div>
      
      {/* Input Section */}
      <div className="mb-4">
        <div className="flex items-center gap-2">
          <input
            type="text"
            value={inputString}
            onChange={(e) => setInputString(e.target.value)}
            placeholder="Enter a string to test"
            className="flex-1 p-2 border rounded-md"
          />
          <button 
            onClick={handleTest}
            className="px-4 py-2 bg-green-500 text-white rounded-md"
          >
            Test
          </button>
          {processingSteps.length > 0 && (
            <button 
              onClick={startAnimation}
              className="px-4 py-2 bg-purple-500 text-white rounded-md"
              disabled={isAnimating}
            >
              Animate
            </button>
          )}
        </div>
      </div>
      
      {/* Result */}
      {result && (
        <div className={`p-3 rounded-md mb-4 text-center ${result.accepted ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
          {result.message}
        </div>
      )}
      
      {/* Processing Steps */}
      {processingSteps.length > 1 && (
        <div className="mb-4">
          <h3 className="font-bold mb-2">Processing Steps:</h3>
          <div className="border rounded-md p-2 bg-white">
            {processingSteps.map((step, index) => (
              <div 
                key={index} 
                className={`p-2 ${index === animationFrame ? 'bg-yellow-100 font-bold' : 'border-b'}`}
              >
                <span className="font-mono">
                  {index === 0 
                    ? 'Start state' 
                    : `Read '${step.symbol}' → ${step.states.length > 0 
                        ? `Now in state(s): ${step.states.join(', ')}` 
                        : 'No valid transitions'}`
                  }
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {/* Example Strings */}
      <div>
        <h3 className="font-bold mb-2">Example Strings:</h3>
        <div className="flex flex-wrap gap-2">
          {exampleStrings.map((str) => (
            <button
              key={str}
              onClick={() => {
                setInputString(str);
                processString(str);
              }}
              className="px-3 py-1 bg-gray-200 rounded-md hover:bg-gray-300"
            >
              {str}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default FSMVisualizer;