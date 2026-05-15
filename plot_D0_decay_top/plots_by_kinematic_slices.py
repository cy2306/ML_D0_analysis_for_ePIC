# Plot distributions for Q^2 > 1 and Q^2 > 100 runs on same figures to compare.
from ROOT import (
    TFile, TH1F, TH2F, TH3F, TCanvas, TPad, TLegend, TPaveText, gPad,
    kRed, kMagenta, kPink, kOrange, kBlack, kBlue, kGreen, kViolet, kCyan, kSpring
)

def multislice_plot(
    th3f, nslices, start_slice, end_slice, var,
    lrange="all", title="ProjectionZ slices", yname="",
    run="1run", legend_loc="right", norm="integral"
):
    """
    Create one plot of z variable with multiple slices of x or y variable.
    """
    histname = th3f.GetName()

    if var == "x":
        nbins = th3f.GetNbinsX()
    elif var == "y":
        nbins = th3f.GetNbinsY()
    else:
        raise ValueError("'var' should be 'x' or 'y' to specify the axis to slice")
    
    delta_n = nbins // nslices

    # Set up canvas
    canvas = TCanvas("c{}_{}".format(histname, var))

    if legend_loc == "right":
        legend = TLegend(0.53, 0.65, 0.85, 0.85)
    else:
        legend = TLegend(0.15, 0.65, 0.4, 0.85)
    legend.SetLineWidth(0)
    legend.SetTextSize(0.035)

    # Histogram styles
    lmarkerstyles = [20, 20, 20, 20, 20]
    llinestyles = [1, 1, 1, 1, 1]   # [2, 2, 1, 1, 1]
    llinewidths = [3, 3, 3, 2, 2]   # [2, 2, 1, 1, 1]
    lcolors = [kBlue+3, kRed-4, kSpring+2, kOrange, kMagenta]  # [kViolet+8, kRed-7, kGreen+1, kOrange, kMagenta]
    
    lclones = [None] * (end_slice - start_slice)

    binlow = start_slice * delta_n + 1
    for islice in range(end_slice - start_slice):
        if var == "x":
            if lrange == "all":
                ylow = 1
                yhigh = th3f.GetNbinsY()
            
            else:
                ylow = th3f.GetYaxis().FindBin(lrange[0])
                yhigh = th3f.GetYaxis().FindBin(lrange[1])
                if lrange[0] > th3f.GetYaxis().GetBinLowEdge(ylow):
                    ylow += 1
                if lrange[1] == th3f.GetYaxis().GetBinLowEdge(yhigh):
                    yhigh -= 1

            xlow = binlow
            xhigh = binlow + delta_n - 1
            
            varname = th3f.GetXaxis().GetTitle()
            if yname == "":
                rangename = th3f.GetYaxis().GetTitle()
            else:
                rangename = yname
            slice_min = th3f.GetXaxis().GetBinLowEdge(xlow)
            slice_max = th3f.GetXaxis().GetBinUpEdge(xhigh)
        
        elif var == "y":
            if lrange == "all":
                xlow = 1
                xhigh = th3f.GetNbinsX()
            else:
                xlow = th3f.GetXaxis().FindBin(lrange[0])
                xhigh = th3f.GetXaxis().FindBin(lrange[1])
                if lrange[0] > th3f.GetXaxis().GetBinLowEdge(xlow):
                    xlow += 1
                if lrange[1] == th3f.GetXaxis().GetBinLowEdge(xhigh):
                    xhigh -= 1

            ylow = binlow
            yhigh = binlow + delta_n - 1
            
            if yname == "":
                varname = th3f.GetYaxis().GetTitle()
            else:
                varname = "y"
            rangename = th3f.GetXaxis().GetTitle()
            slice_min = th3f.GetYaxis().GetBinLowEdge(ylow)
            slice_max = th3f.GetYaxis().GetBinUpEdge(yhigh)
        
        binlow += delta_n

        if lrange == "all":
            proj_name = "{}Slices".format(var)
        elif isinstance(lrange, list):
            proj_name = "{}Slices_Range{}to{}".format(var, lrange[0], lrange[1])
        else:
            raise TypeError(
                "'lrange' should be a list with 2 numbers [low_edge, high_edge], or 'none' otherwise"
            )

        proj = th3f.ProjectionZ("{}_{}_Num{}".format(histname, proj_name, islice),
            xlow, xhigh, ylow, yhigh)
        
        
        # Normalize events
        if norm == "integral":
            try:
                proj.Scale(1 / proj.Integral())
                proj.GetYaxis().SetTitle("Fraction of total events")
            except(ZeroDivisionError):
                pass
            ymax = 1.
        
        elif norm == "none":
            proj.GetYaxis().SetTitle("Events")
        else:
            raise ValueError("'norm' should be 'integral' or 'none'")

        # Clone histogram
        lclones[islice] = proj.Clone(
            "{}_{}_Num{}_clone".format(histname, proj_name, islice)
        )
        lclones[islice].SetMaximum(1.2 * ymax)
        if lrange == "all":
            lclones[islice].SetTitle(title)
        else:
            lclones[islice].SetTitle(
                "{} ({} < {} < {})".format(title, lrange[0], rangename, lrange[1])
            )
        lclones[islice].GetYaxis().SetTitle(proj.GetYaxis().GetTitle())
        lclones[islice].GetYaxis().SetTitleSize(0.04)
        lclones[islice].GetXaxis().SetTitleSize(0.04)

        # Set hist style
        lclones[islice].SetMarkerStyle(lmarkerstyles[islice])
        lclones[islice].SetLineWidth(llinewidths[islice])
        lclones[islice].SetMarkerSize(0.5)
        lclones[islice].SetLineStyle(llinestyles[islice])
        lclones[islice].SetLineColor(lcolors[islice])
        lclones[islice].SetMarkerColor(lcolors[islice])
        lclones[islice].SetStats(0)
    
        # Draw
        if islice == 0:
            lclones[0].Draw("hist")
        else:
            lclones[islice].Draw("hist same")
        gPad.SetLogy()
        
        legend.AddEntry(
            lclones[islice],
            "{:.2f} < {} < {:.2f}".format(slice_min, varname, slice_max), "l"
        )
    
    legend.Draw()
    canvas.Print("hq2_100_{}_{}_multi_{}.pdf".format(run, histname, proj_name))


def multiplot_by_slices(
    th3f_bkg1, th3f_sig1, th3f_bkg100, th3f_sig100, nslices, var,
    lrange="all", title="ProjectionZ", yname="",
    run="1run", legend_loc="right", norm="integral",
    sig_only=False, single_q2=False
):
    """
    Create plot of z variable for each slice of x or y variable.
    """
    histname_bkg = th3f_bkg1.GetName()
    histname_sig = th3f_sig1.GetName()
    if var == "x":
        nbins = th3f_sig1.GetNbinsX()
    elif var == "y":
        nbins = th3f_sig1.GetNbinsY()
    else:
        raise ValueError("'var' should be 'x' or 'y' to specify the axis to slice")
    
    delta_n = nbins // nslices

    # Set up canvas and plots
    lcanvases = []
    ncanvases = nslices // 4 + 1
    for c in range(ncanvases):
        canvas = TCanvas("c{}_{}_{}_r{}to{}".format(
            c, histname_bkg, var, lrange[0], lrange[1]
        ))
        canvas.Divide(2, 2)
        lcanvases.append(canvas)

    llegends = []
    for n in range(nslices):
        if legend_loc == "right":
            legend = TLegend(0.6, 0.65, 0.85, 0.85)
        else:
            legend = TLegend(0.15, 0.65, 0.4, 0.85)
        legend.SetLineWidth(0)
        legend.SetTextSize(0.04)
        llegends.append(legend)

    lbkg1_clones = [None] * nslices
    lsig1_clones = [None] * nslices
    lbkg100_clones = [None] * nslices
    lsig100_clones = [None] * nslices

    llbkg_clones = [lbkg1_clones, lbkg100_clones]
    llsig_clones = [lsig1_clones, lsig100_clones]

    lproj_bkg = [None] * 2
    lproj_sig = [None] * 2
    
    binlow = 1
    for islice in range(nslices):    # loop over all slices of variable
        if var == "x":
            if lrange == "all":
                ylow = 1
                yhigh = th3f_bkg1.GetNbinsY()
            
            else:
                ylow = th3f_bkg1.GetYaxis().FindBin(lrange[0])
                yhigh = th3f_bkg1.GetYaxis().FindBin(lrange[1])
                if lrange[0] > th3f_bkg1.GetYaxis().GetBinLowEdge(ylow):
                    ylow += 1
                if lrange[1] == th3f_bkg1.GetYaxis().GetBinLowEdge(yhigh):
                    yhigh -= 1
            
            xlow = binlow
            xhigh = binlow + delta_n - 1

            varname = th3f_bkg1.GetXaxis().GetTitle()
            if yname == "":
                rangename = th3f_bkg1.GetYaxis().GetTitle()
            else:
                rangename = yname
            slice_min = th3f_bkg1.GetXaxis().GetBinLowEdge(xlow)
            slice_max = th3f_bkg1.GetXaxis().GetBinUpEdge(xhigh)
        
        elif var == "y":
            if lrange == "all":
                xlow = 1
                xhigh = th3f_bkg1.GetNbinsX()
            else:
                xlow = th3f_bkg1.GetXaxis().FindBin(lrange[0])
                xhigh = th3f_bkg1.GetXaxis().FindBin(lrange[1])
                if lrange[0] > th3f_bkg1.GetXaxis().GetBinLowEdge(xlow):
                    xlow += 1
                if lrange[1] == th3f_bkg1.GetXaxis().GetBinLowEdge(xhigh):
                    xhigh -= 1

            ylow = binlow
            yhigh = binlow + delta_n - 1
            
            if yname == "":
                varname = th3f_bkg1.GetYaxis().GetTitle()
            else:
                varname = yname
            rangename = th3f_bkg1.GetXaxis().GetTitle()
            slice_min = th3f_bkg1.GetYaxis().GetBinLowEdge(ylow)
            slice_max = th3f_bkg1.GetYaxis().GetBinUpEdge(yhigh)
        
        binlow += delta_n

        if lrange == "all":
            proj_name = "{}Slices".format(var)
        elif isinstance(lrange, list):
            proj_name = "{}Slices_Range{}to{}".format(var, lrange[0], lrange[1])
        else:
            raise TypeError(
                "'lrange' should be a list with 2 numbers [low_edge, high_edge], or 'none' otherwise"
            )

        lproj_bkg[0] = th3f_bkg1.ProjectionZ(
            "{}_{}_Num{}_1".format(histname_bkg, proj_name, islice),
            xlow, xhigh, ylow, yhigh
        )
        lproj_sig[0] = th3f_sig1.ProjectionZ(
            "{}_{}_Num{}_1".format(histname_sig, proj_name, islice),
            xlow, xhigh, ylow, yhigh
        )
        lproj_bkg[1] = th3f_bkg100.ProjectionZ(
            "{}_{}_Num{}_100".format(histname_bkg, proj_name, islice),
            xlow, xhigh, ylow, yhigh
        )
        lproj_sig[1] = th3f_sig100.ProjectionZ(
            "{}_{}_Num{}_100".format(histname_sig, proj_name, islice),
            xlow, xhigh, ylow, yhigh
        )
        
        # Normalize events
        if norm == "integral":
            for q in range(2):  # loop over Q^2 ranges (> 1, > 100)
                try:
                    lproj_bkg[q].Scale(1 / lproj_bkg[q].Integral())
                    lproj_bkg[q].GetYaxis().SetTitle("Fraction of total events")
                    lproj_sig[q].Scale(1 / lproj_sig[q].Integral())
                    lproj_sig[q].GetYaxis().SetTitle("Fraction of total events")
                except(ZeroDivisionError):
                    pass
                ymax = 1.
        
        elif norm == "none":
            for q in range(2):
                lproj_bkg[q].GetYaxis().SetTitle("Events")
                lproj_sig[q].GetYaxis().SetTitle("Events")
            ymax = max([
                lproj_bkg[0].GetMaximum(), lproj_bkg[1].GetMaximum(),
                lproj_sig[0].GetMaximum(), lproj_sig[1].GetMaximum()
            ])
        else:
            raise ValueError("'norm' should be 'integral' or 'none'")

        # Clone histograms
        lbkg1_clones[islice] = lproj_bkg[0].Clone(
            "{}_{}_Num{}_1_clone".format(histname_bkg, proj_name, islice)
        )
        lbkg1_clones[islice].SetMaximum(1.2 * ymax)

        lsig1_clones[islice] = lproj_sig[0].Clone(
            "{}_{}_Num{}_1_clone".format(histname_sig, proj_name, islice)
        )
        lsig1_clones[islice].SetMaximum(1.2 * ymax)

        lbkg100_clones[islice] = lproj_bkg[1].Clone(
            "{}_{}_Num{}_100_clone".format(histname_bkg, proj_name, islice)
        )
        lbkg100_clones[islice].SetMaximum(1.2 * ymax)

        lsig100_clones[islice] = lproj_sig[1].Clone(
            "{}_{}_Num{}_100_clone".format(histname_sig, proj_name, islice)
        )
        lsig100_clones[islice].SetMaximum(1.2 * ymax)
        

        if lrange == "all":
            lbkg1_clones[islice].SetTitle(
                "{} for {:.2f} < {} < {:.2f}".format(title, slice_min, varname, slice_max)
            )
            lsig1_clones[islice].SetTitle(
                "{} for {:.2f} < {} < {:.2f}".format(title, slice_min, varname, slice_max)
            )
            lbkg100_clones[islice].SetTitle(
                "{} for {:.2f} < {} < {:.2f}".format(title, slice_min, varname, slice_max)
            )
            lsig100_clones[islice].SetTitle(
                "{} for {:.2f} < {} < {:.2f}".format(title, slice_min, varname, slice_max)
            )
        else:
            lbkg1_clones[islice].SetTitle(
                "{} for {:.2f} < {} < {:.2f} ({} < {} < {})".format(
                    title, slice_min, varname, slice_max, lrange[0], rangename, lrange[1]
            ))
            lsig1_clones[islice].SetTitle(
                "{} for {:.2f} < {} < {:.2f} ({} < {} < {})".format(
                    title, slice_min, varname, slice_max, lrange[0], rangename, lrange[1]
            ))
            lbkg100_clones[islice].SetTitle(
                "{} for {:.2f} < {} < {:.2f} ({} < {} < {})".format(
                    title, slice_min, varname, slice_max, lrange[0], rangename, lrange[1]
            ))
            lsig100_clones[islice].SetTitle(
                "{} for {:.2f} < {} < {:.2f} ({} < {} < {})".format(
                    title, slice_min, varname, slice_max, lrange[0], rangename, lrange[1]
            ))
        
        lbkg1_clones[islice].GetYaxis().SetTitle(lproj_bkg[0].GetYaxis().GetTitle())
        lbkg1_clones[islice].GetYaxis().SetTitleSize(0.04)
        lbkg1_clones[islice].GetXaxis().SetTitleSize(0.04)

        lsig1_clones[islice].GetYaxis().SetTitle(lproj_bkg[0].GetYaxis().GetTitle())
        lsig1_clones[islice].GetYaxis().SetTitleSize(0.04)
        lsig1_clones[islice].GetXaxis().SetTitleSize(0.04)

        lbkg100_clones[islice].GetYaxis().SetTitle(lproj_bkg[0].GetYaxis().GetTitle())
        lbkg100_clones[islice].GetYaxis().SetTitleSize(0.04)
        lbkg100_clones[islice].GetXaxis().SetTitleSize(0.04)

        lsig100_clones[islice].GetYaxis().SetTitle(lproj_bkg[0].GetYaxis().GetTitle())
        lsig100_clones[islice].GetYaxis().SetTitleSize(0.04)
        lsig100_clones[islice].GetXaxis().SetTitleSize(0.04)

        # lbkg100_clones[islice] = lproj_bkg[1].Clone(
        #     "{}_{}Slices_Num{}_100_clone".format(histname_bkg, var, islice)
        # )
        # lsig100_clones[islice] = lproj_sig[1].Clone(
        #     "{}_{}Slices_Num{}_100_clone".format(histname_sig, var, islice)
        # )

        # Set hist styles
        lbkg_linewidths = [1, 1]
        lbkg_linestyles = [1, 1]    # solid
        lsig_markerstyles = [20, 21]    # circle, square
        lcolors_bkg = [kPink+1, kBlue-8]
        lcolors_sig = [kPink, kBlue+2]
        for q in range(2):
            llbkg_clones[q][islice].SetLineWidth(lbkg_linewidths[q])
            llbkg_clones[q][islice].SetLineStyle(lbkg_linestyles[q])        # solid line
            llbkg_clones[q][islice].SetLineColor(lcolors_bkg[q])
            llbkg_clones[q][islice].SetStats(0)

            llsig_clones[q][islice].SetMarkerStyle(lsig_markerstyles[q])     # circle
            llsig_clones[q][islice].SetMarkerSize(0.5)
            llsig_clones[q][islice].SetLineColor(lcolors_sig[q])
            llsig_clones[q][islice].SetMarkerColor(lcolors_sig[q])
            llsig_clones[q][islice].SetStats(0)
        
        # Draw
        c = islice // 4
        pad = islice % 4 + 1
        lcanvases[c].cd(pad)

        if single_q2:
            lbkg100_clones[islice].Draw("hist")
            lsig100_clones[islice].Draw("p same")
            lsig100_clones[islice].Draw("e0 same")
        else:
            if sig_only:
                lsig1_clones[islice].Draw("p")
            else:
                lbkg1_clones[islice].Draw("hist")
                lbkg100_clones[islice].Draw("hist same")
                lsig1_clones[islice].Draw("p same")
            
            lsig1_clones[islice].Draw("e0 same")
            lsig100_clones[islice].Draw("p same")
            lsig100_clones[islice].Draw("e0 same")
        gPad.SetLogy()

        if sig_only:
            llegends[islice].AddEntry(
            lsig1_clones[islice], "{} > 1 signal".format("Q^{2}"), "lp"
            )
            llegends[islice].AddEntry(
            lsig100_clones[islice], "{} > 100 signal".format("Q^{2}"), "lp"
            )
        else:
            if not single_q2:
                llegends[islice].AddEntry(
                    lsig1_clones[islice], "{}, {} > 1".format("D^{0} to #piK", "Q^{2}"), "lp"
                )
                llegends[islice].AddEntry(
                    lbkg1_clones[islice], "Bkg, {} > 1".format("Q^{2}"), "l"
                )
            llegends[islice].AddEntry(
                lsig100_clones[islice], "{}, {} > 100".format("D^{0} to #piK", "Q^{2}"), "lp"
            )
            llegends[islice].AddEntry(
                lbkg100_clones[islice], "Bkg, {} > 100".format("Q^{2}"), "l"
            )
        llegends[islice].Draw()
    
    for c in range(ncanvases):
        if sig_only:
            lcanvases[c].Print("hq2_comp_{}_sigonly_{}_by_{}_{}.pdf".format(
            run, histname_sig, proj_name, c
        ))
        elif single_q2:
            lcanvases[c].Print("hq2_comp_{}_100only_{}_by_{}_{}.pdf".format(
            run, histname_sig, proj_name, c
        ))
        else:
            lcanvases[c].Print("hq2_comp_{}_{}_by_{}_{}.pdf".format(
                run, histname_sig, proj_name, c
            ))
    print("--- Multiplots done: {} by {} slices for range {} t0 {}".format(
        title, varname, lrange[0], lrange[1]
    ))


def pik_pt_eta_multiplot(infile1, infile100, run, sig_only=False):
    """
    Plot pt and eta of D0-decayed (secondary) and bkg (primary)
    pions and kaons. Draw Q^2 > 1 and Q^2 > 100 data on the same graphs to compare.
    Plots projected from 3D histograms of DCA vs. pT and eta.
    
    Args:
    infile1, infile100 (TFile): root files with Q^2 > 1 and Q^2 > 100 histograms

    Outputs:
    Prints pdf of canvas containing plots.
    Returns: None
    """
    lrun_names = ["q2_1", "q2_100"]
    lpart_names = ["Pi", "K"]
    lpart_titles = ["#pi", "K"]
    lvar_titles = ["p_{T}", "#eta"]

    # Set up canvas
    canvas = TCanvas("cpik_pt_eta")
    canvas.cd()

    low = 0.02
    mid1 = 0.5
    mid2 = 0.52
    high = 1
    pad1 = TPad("ppi_pt", "", low, mid2, mid1, high)
    pad2 = TPad("ppi_eta", "", mid2, mid2, high, high)
    pad3 = TPad("pk_pt", "", low, low, mid1, mid1)
    pad4 = TPad("pk_eta", "", mid2, low, high, mid1)
    lpads = [pad1, pad2, pad3, pad4]
    for p in range(4):
        if p % 2 == 0:
            lpads[p].SetLogy()
        lpads[p].Draw()

    llegends = []
    for _ in range(2):
        legend1 = TLegend(0.45, 0.65, 0.65, 0.85)
        legend1.SetLineWidth(0)
        legend1.SetTextSize(0.04)
        llegends.append(legend1)

        legend2 = TLegend(0.15, 0.65, 0.35, 0.85)
        legend2.SetLineWidth(0)
        legend2.SetTextSize(0.04)
        llegends.append(legend2)
    
    
    lbkg1_clones = [None] * 4
    lsig1_clones = [None] * 4
    lbkg100_clones = [None] * 4
    lsig100_clones = [None] * 4

    llbkg_clones = [lbkg1_clones, lbkg100_clones]
    llsig_clones = [lsig1_clones, lsig100_clones]

    pad = 0
    for i in range(2):      # loop over particle types
        histname_bkg = "hRcPrim{}LocaToRCVtx".format(lpart_names[i])
        histname_sig = "hRcSec{}LocaToRCVtx".format(lpart_names[i])

        for j in range(2):      # loop over variable types (pt, eta)
            lhbkg = [infile1.Get(histname_bkg), infile100.Get(histname_bkg)]
            lhsig = [infile1.Get(histname_sig), infile100.Get(histname_sig)]

            lproj_bkg = [None, None]
            lproj_sig = [None, None]
            for q in range(2):
                if j == 0:
                    lproj_bkg[q] = lhbkg[q].ProjectionX(
                        "{}_projPt_{}".format(histname_bkg, lrun_names[q])
                    )
                    lproj_sig[q] = lhsig[q].ProjectionX(
                        "{}_projPt_{}".format(histname_sig, lrun_names[q])
                    )
                else:
                    lproj_bkg[q] = lhbkg[q].ProjectionY(
                        "{}_projEta_{}".format(histname_bkg, lrun_names[q])
                    )
                    lproj_sig[q] = lhsig[q].ProjectionY(
                        "{}_projEta_{}".format(histname_sig, lrun_names[q])
                    )

                lproj_bkg[q].Scale(1 / lproj_bkg[q].Integral())
                lproj_bkg[q].GetYaxis().SetTitle("Fraction of total events")
                lproj_sig[q].Scale(1 / lproj_sig[q].Integral())
                lproj_sig[q].GetYaxis().SetTitle("Fraction of total events")
            
            ymax = max([
                lproj_bkg[0].GetMaximum(), lproj_bkg[1].GetMaximum(),
                lproj_sig[0].GetMaximum(), lproj_sig[1].GetMaximum()
            ])


            # Clone histograms
            lbkg1_clones[pad] = lproj_bkg[0].Clone(histname_bkg+"q2_1_clone")
            lbkg1_clones[pad].SetMaximum(1.2 * ymax)
            lbkg1_clones[pad].SetTitle(
                "{} of {} decayed and primary {}".format(lvar_titles[j], "D^{0}", lpart_titles[i])
            )
            lbkg1_clones[pad].GetXaxis().SetTitleOffset(0.9)
            lbkg1_clones[pad].GetXaxis().SetTitleSize(0.05)
            lbkg1_clones[pad].GetXaxis().SetLabelSize(0.04)
            lbkg1_clones[pad].GetYaxis().SetTitleOffset(1.1)
            lbkg1_clones[pad].GetYaxis().SetTitleSize(0.05)
            lbkg1_clones[pad].GetYaxis().SetLabelSize(0.04)

            lsig1_clones[pad] = lproj_sig[0].Clone(histname_sig+"q2_1_clone")
            if sig_only:
                lsig1_clones[pad].SetMaximum(1.2 * ymax)
                lsig1_clones[pad].SetTitle(
                    "{} of {} decayed {}".format(lvar_titles[j], "D^{0}", lpart_titles[i])
                )
                lsig1_clones[pad].GetXaxis().SetTitleOffset(0.9)
                lsig1_clones[pad].GetXaxis().SetTitleSize(0.05)
                lsig1_clones[pad].GetXaxis().SetLabelSize(0.04)
                lsig1_clones[pad].GetYaxis().SetTitleOffset(1.)
                lsig1_clones[pad].GetYaxis().SetTitleSize(0.05)
                lsig1_clones[pad].GetYaxis().SetLabelSize(0.04)
            
            lbkg100_clones[pad] = lproj_bkg[1].Clone(histname_bkg+"_q2_100_clone")
            lsig100_clones[pad] = lproj_sig[1].Clone(histname_sig+"q2_100_clone")

            # Set hist styles
            lbkg_linewidths = [1, 2]
            lbkg_linestyles = [1, 3]    # solid, dotted
            lsig_markerstyles = [20, 21]    # circle, square
            lcolors = [kPink, kBlue+2]
            for q in range(2):
                llbkg_clones[q][pad].SetLineWidth(lbkg_linewidths[q])
                llbkg_clones[q][pad].SetLineStyle(lbkg_linestyles[q])        # solid line
                llbkg_clones[q][pad].SetLineColor(lcolors[q])
                llbkg_clones[q][pad].SetStats(0)

                llsig_clones[q][pad].SetMarkerStyle(lsig_markerstyles[q])     # circle
                llsig_clones[q][pad].SetMarkerSize(0.6)
                llsig_clones[q][pad].SetLineColor(lcolors[q])
                llsig_clones[q][pad].SetMarkerColor(lcolors[q])
                llsig_clones[q][pad].SetStats(0)

            # Draw
            lpads[pad].cd()
            if sig_only:
                llsig_clones[0][pad].Draw("p")
            else:
                llbkg_clones[0][pad].Draw("hist")
                llbkg_clones[1][pad].Draw("hist same")

            llsig_clones[0][pad].Draw("p same")
            llsig_clones[0][pad].Draw("e0 same")
            llsig_clones[1][pad].Draw("p same")
            llsig_clones[1][pad].Draw("e0 same")
            
            if sig_only:
                llegends[pad].AddEntry(
                llsig_clones[0][pad],
                "{} > 1 signal".format("Q^{2}"), "lp"
                )
                llegends[pad].AddEntry(
                    llsig_clones[1][pad],
                    "{} > 100 signal".format("Q^{2}"), "lp"
                )
            else:
                llegends[pad].AddEntry(
                    llsig_clones[0][pad],
                    "{} decayed {}, {} > 1".format("D^{0}", lpart_titles[i], "Q^{2}"), "lp"
                )
                llegends[pad].AddEntry(
                    llbkg_clones[0][pad],
                    "Primary {}, {} > 1".format(lpart_titles[i], "Q^{2}"), "l"
                )
                llegends[pad].AddEntry(
                    llsig_clones[1][pad],
                    "{} decayed {}, {} > 100".format("D^{0}", lpart_titles[i], "Q^{2}"), "lp"
                )
                llegends[pad].AddEntry(
                    llbkg_clones[1][pad],
                    "Primary {}, {} > 100".format(lpart_titles[i], "Q^{2}"), "l"
                )
            llegends[pad].Draw()

            pad += 1
    
    if sig_only:
        canvas.Print("hq2_comp_{}_sigonly_piK_pteta.pdf".format(run))
    else:
        canvas.Print("hq2_comp_{}_piK_pteta.pdf".format(run))
    print("--- Multiplots done: pt and eta of pi/K")


def main():
    run = "50runs"
    infile1 = TFile("/home/cy2306/eic/vertexing_D0/ePIC/HF_reco/helix/q2_1_50runs.root", "READ")
    infile100 = TFile("/home/cy2306/eic/vertexing_D0/ePIC/HF_reco/helix/q2_100_50runs.root", "READ")
    
    # pik_pt_eta_multiplot(infile1, infile100, run, sig_only=True)

    # piK DCA plots
    lpart_names = ["Pi", "K"]
    lpart_titles = ["#pi", "K"]
    ldca_names = ["a", "b"]
    ldca_titles = ["DCA_{xy}", "DCA_{z}"]

    for i in range(2):      # loop over particle types
        for j in range(2):      # loop over DCA types
            histname_bkg = "hRcPrim{}Loc{}ToRCVtx".format(lpart_names[i], ldca_names[j])
            histname_sig = "hRcSec{}Loc{}ToRCVtx".format(lpart_names[i], ldca_names[j])

            hbkg1 = infile1.Get(histname_bkg)
            hsig1 = infile1.Get(histname_sig)
            hbkg100 = infile100.Get(histname_bkg)
            hsig100 = infile100.Get(histname_sig)


            title = "{} of {}".format(ldca_titles[j], lpart_titles[i])
            title2 = "{} of {} for {} signal".format(
                ldca_titles[j], lpart_titles[i], "Q^{2} > 100"
            )
            # multiplot_by_slices(
            #     hbkg1, hsig1, hbkg100, hsig100, 10, "x", title=title, run=run
            # )
            # multiplot_by_slices(
            #     hbkg1, hsig1, hbkg100, hsig100, 10, "y", title=title, run=run,
            #     sig_only=False
            #     )

            # multislice_plot(
            #     hsig100, 10, 0, 4, "x", title=title2, run=run
            # )
            # multislice_plot(
            #     hsig100, 10, 3, 8, "y", title=title2, run=run
            # )

            # Simultaneous slices in pt and eta.
            # lranges_eta = [[-5, -1], [-1, 1], [-1, 0], [0, 1], [1, 5]]
            lranges_eta = [[-1, 1], [1, 5]]
            for k in range(len(lranges_eta)):
                multiplot_by_slices(
                    hbkg1, hsig1, hbkg100, hsig100, 10, "x",
                    lrange=lranges_eta[k], title=title, run=run,
                    sig_only=False, single_q2=True
                )

                # multislice_plot(
                #     hsig100, 10, 1, 4, "x",
                #     lrange=lranges_eta[k], title=title2, run=run
                # )

            # lranges_pt = [[0, 1], [1, 2], [0, 2], [2, 4], [4, 10]]
            lranges_pt = [[0, 2], [2, 4]]
            for k in range(len(lranges_pt)):
                multiplot_by_slices(
                    hbkg1, hsig1, hbkg100, hsig100, 10, "y",
                    lrange=lranges_pt[k], title=title, run=run,
                    sig_only=False, single_q2=True
                )

                # multislice_plot(
                #     hsig100, 10, 5, 8, "y",
                #     lrange=lranges_pt[k], title=title2, run=run
                # )
    
    
    # plots for DCA_12, cos(theta), DCA_D0, and decay length
    lvar_names = ["Dca12", "CosTheta", "Dca", "DecayLength"]
    lvar_titles = ["DCA_{12}", "cos(#theta)", "DCA", "Decay length"]
    # lvar_names = ["Dca12"]
    # lvar_titles = ["DCA_{12}"]

    for i in range(len(lvar_names)):  # loop over variables to plot
        # histname_bkg = "h3Pair{}_bkg".format(lvar_names[i])
        # histname_sig = "h3Pair{}_signal".format(lvar_names[i])
        histname_bkg = "h3Pair{}_MCvtx_bkg".format(lvar_names[i])
        histname_sig = "h3Pair{}_MCvtx_signal".format(lvar_names[i])

        hbkg1 = infile1.Get(histname_bkg)
        hsig1 = infile1.Get(histname_sig)
        hbkg100 = infile100.Get(histname_bkg)
        hsig100 = infile100.Get(histname_sig)
    
        title = "{} of #piK pair".format(lvar_titles[i])
        title2 = "{} of #piK pair for {} signal".format(lvar_titles[i], "Q^{2} > 100")
        
        # multiplot_by_slices(
        #     hbkg1, hsig1, hbkg100, hsig100, 10, "x",
        #     title=title, run=run, sig_only=False, yname="y"
        # )
        # multiplot_by_slices(
        #     hbkg1, hsig1, hbkg100, hsig100, 10, "y", title=title, run=run,
        #     sig_only=False, single_q2=True
        #     )

        # multislice_plot(
        #     hsig100, 10, 0, 4, "x", title=title2, run=run
        # )
        # multislice_plot(
        #     hsig100, 10, 3, 8, "y", title=title2, run=run
        # )
        
        # Simultaneous slices in pt and eta.
        # lranges_eta = [[-1, 1], [1, 5]]
        # for k in range(len(lranges_eta)):
        #     multiplot_by_slices(
        #         hbkg1, hsig1, hbkg100, hsig100, 10, "x",
        #         lrange=lranges_eta[k], title=title, run=run,
        #         sig_only=True, yname="y"
        #     )

        #     multislice_plot(
        #         hsig100, 10, 1, 4, "x",
        #         lrange=lranges_eta[k], title=title2, run=run
        #     )

        # lranges_pt = [[0, 2], [2, 4]]
        # for k in range(len(lranges_pt)):
        #     multiplot_by_slices(
        #         hbkg1, hsig1, hbkg100, hsig100, 10, "y",
        #         lrange=lranges_pt[k], title=title, run=run,
        #         sig_only=True, single_q2=False, yname="y"
        #     )

        #     multislice_plot(
        #         hsig100, 10, 5, 8, "y",
        #         lrange=lranges_pt[k], title=title2, run=run, yname="y"
        #     )


    
    
    # invariant mass plots
    # lcut_names = ["all", "DCA"]
    # lcut_titles = ["all", "after DCA cuts"]

    # for i in range(2):  # loop over cuts
    #     histname_bkg = "h3InvMass_bkg_{}".format(lcut_names[i])
    #     histname_sig = "h3InvMass_signal_{}".format(lcut_names[i])

    #     hbkg1 = infile1.Get(histname_bkg)
    #     hsig1 = infile1.Get(histname_sig)
    #     hbkg100 = infile100.Get(histname_bkg)
    #     hsig100 = infile100.Get(histname_sig)

    #     title = "Invariant mass of #piK pair ({})".format(lcut_titles[i])
        # multiplot_by_slices(
        #     hbkg1, hsig1, hbkg100, hsig100, 10, "x", title, run, legend_loc="left", norm="none"
        # )
        # multiplot_by_slices(
        #     hbkg1, hsig1, hbkg100, hsig100, 10, "y", title, run, legend_loc="left", norm="none"
        # )

        # multislice_plot(
        #     hsig100, 10, 0, 4, "x", title, run, legend_loc="left"
        # )
        # multislice_plot(
        #     hsig100, 10, 3, 8, "y", title, run, legend_loc="left"
        # )



if __name__ == "__main__":
    main()
