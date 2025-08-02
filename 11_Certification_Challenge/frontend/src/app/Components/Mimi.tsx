"use client"

import { CopilotChat, useCopilotChatSuggestions } from "@copilotkit/react-ui"
import { suggestionPrompt } from "../prompts"
import { useCoAgent, useCoAgentStateRender, useCopilotAction, useCopilotChat } from "@copilotkit/react-core"
import { useEffect, useState, useRef } from "react"
import Image from "next/image"


export const Mimi = () => {
    const { visibleMessages } = useCopilotChat()
    
    const respondedRef = useRef(false)
    
    const {
        state: agentState,
        nodeName
    } = useCoAgent<{
        question: string;
    }>({
        name: "Mimi",
        initialState: {
            question: ""
        }
    })
    
    
    
    useCopilotChatSuggestions({
        instructions: suggestionPrompt,
        minSuggestions: 1,
        maxSuggestions: 6,
    })


    return (
        <div className="w-screen bg-white flex flex-col overflow-hidden" style={{ height: '100vh' }}>
            {/* Logo in the top left */}
            <div className="p-8 bg-white flex items-center">
                <div className="flex items-center mr-4">
                    <Image 
                        src="/skillenai_logo.png" 
                        alt="Skillenai Logo" 
                        width={180} 
                        height={60}
                    />
                </div>
            </div>
            
            {/* Welcome message that disappears when there are messages */}
            {visibleMessages.length === 0 && (
                <div className="absolute top-[25%] left-0 right-0 mx-auto w-full max-w-3xl z-40 pl-10">
                    <h1 className="text-4xl font-bold text-black mb-3">Hello, I am Mimi!</h1>
                    <p className="text-2xl text-gray-500">I can help you develop an AI strategy for your business.</p>
                </div>
            )}
            
            <div className="flex-1 flex justify-center items-center bg-white overflow-y-auto">
                <CopilotChat className="w-full max-w-3xl flex flex-col h-full py-6" />
            </div>
        </div>
    )
}
