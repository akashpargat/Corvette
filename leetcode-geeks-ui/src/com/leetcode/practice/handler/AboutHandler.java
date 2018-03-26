package com.leetcode.practice.handler;

import org.eclipse.e4.core.di.annotations.Execute;
import org.eclipse.jface.dialogs.MessageDialog;
import org.eclipse.swt.widgets.Shell;

/**
 * @author Cracking Google
 */
public class AboutHandler
{
    @Execute
    public void execute(Shell shell)
    {
        MessageDialog.openInformation(shell, "About", "Eclipse 4 RCP Application");
    }
}