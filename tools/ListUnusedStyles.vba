Sub ListUnusedStyles()
    Dim oStyle As Style

    For Each oStyle In ActiveDocument.Styles
        'Only check out non-built-in styles for paragraphs and characters (ignore tables and lists)
        If oStyle.BuiltIn = False And (oStyle.Type = wdStyleTypeParagraph Or oStyle.Type = wdStyleTypeCharacter) Then
            'Exclude Citavi-Styles
            If InStr(oStyle.NameLocal, "Citavi") = 0 Then
                styleFound = False
                
                'Search main text
                With ActiveDocument.Content.Find
                    .ClearFormatting
                    .Style = oStyle.NameLocal
                    .Execute FindText:="", Format:=True
                    If .Found = True Then styleFound = True
                End With
                    
                'Check headers
                For Each oSection In ActiveDocument.Sections
                    For Each oHeader In oSection.Headers
                        If oHeader.Exists Then
                           'oHeader.Range.Collapse Direction:=wdCollapseStart
                            With oHeader.Range.Find
                                .ClearFormatting
                                .Style = oStyle
                                .Forward = True
                                .Format = True
                                .Text = ""
                                .Execute
                                
                                If .Found = True Then styleFound = True
                            End With
                        End If
                        If styleFound = True Then Exit For
                    Next oHeader
                    If styleFound = True Then Exit For
                Next oSection
                            
                'Output style if not found
                If styleFound = False Then
                    Debug.Print (oStyle.NameLocal)
                End If
            End If
        End If
    Next oStyle
End Sub
