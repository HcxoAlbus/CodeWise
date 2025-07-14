/**
 * 代码编辑器组件
 * 负责人：组员A
 * 作用：基于Monaco Editor的代码输入组件，支持语法高亮和代码补全
 */

import React from 'react'
import Editor from '@monaco-editor/react'

const CodeEditor = ({ 
  value = '', 
  onChange, 
  language = 'python',
  height = '400px',
  theme = 'vs-dark',
  readOnly = false 
}) => {
  const handleEditorChange = (newValue) => {
    if (onChange) {
      onChange(newValue || '')
    }
  }

  const editorOptions = {
    minimap: { enabled: false },
    fontSize: 14,
    lineNumbers: 'on',
    roundedSelection: false,
    scrollBeyondLastLine: false,
    automaticLayout: true,
    tabSize: 4,
    insertSpaces: true,
    wordWrap: 'on',
    readOnly
  }

  return (
    <div className="code-editor-wrapper">
      <Editor
        height={height}
        defaultLanguage={language}
        value={value}
        theme={theme}
        options={editorOptions}
        onChange={handleEditorChange}
        loading={<div>加载编辑器中...</div>}
      />
    </div>
  )
}

export default CodeEditor