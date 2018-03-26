package com.leetcode.practice.handler;

import org.eclipse.e4.core.di.annotations.CanExecute;
import org.eclipse.e4.core.di.annotations.Execute;
import org.eclipse.e4.ui.workbench.modeling.EPartService;

/**
 * @author Cracking Google
 */
public class SaveHandler
{

    @CanExecute
    public boolean canExecute(EPartService partService)
    {
        if (partService != null)
        {
            return !partService.getDirtyParts().isEmpty();
        }
        return false;
    }

    @Execute
    public void execute(EPartService partService)
    {
        partService.saveAll(false);
    }
}