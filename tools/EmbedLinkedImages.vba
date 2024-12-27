Sub EmbedLinkedImages()
    Dim TrkStatus As Boolean
    Dim Rng       As Range
    Dim iShp      As InlineShape
    Dim iCntrl    As CommandBarControl
    
    Set iCntrl = Application.CommandBars.FindControl(ID:=6382)
    
    Application.ScreenUpdating = False
    
    With ActiveDocument
        .Fields.Update
        TrkStatus = .TrackRevisions
        .TrackRevisions = False
        
        For Each Rng In .StoryRanges
            ' Go through the inlineshapes in the story range.
            For Each iShp In Rng.InlineShapes
                If Not iShp.LinkFormat Is Nothing Then
                    iShp.LinkFormat.Update
                    iShp.LinkFormat.SavePictureWithDocument = True
                    iShp.LinkFormat.BreakLink
                End If
            Next iShp
        Next Rng
        .TrackRevisions = TrkStatus
        .Fields.Update
    End With
    
    Application.ScreenUpdating = True
    
    SendKeys "%e~"
    iCntrl.Execute
End Sub
