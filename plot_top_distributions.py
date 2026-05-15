# Make 1d projections of 2d and 3d histograms for D0 decay kinematics.
from ROOT import (
    TFile, TH1F, TH2F, TH3F, TCanvas, TLegend, TPaveText, kRed, kMagenta, kOrange, kBlack
)

def pik_dca_proj(infile, run):
    """
    Plot DCA_xy (loca) and DCA_z (locb) of D0-decayed (secondary) and bkg (primary)
    pions and kaons. Projected from 3D histograms of DCA vs. pT and eta.
    
    Args:
    infile (TFile): root file containing 3D histograms
    run (str): identifying name of the simulation run
    
    Outputs:
    Prints pdf of canvas containing plots.
    Returns: None
    """
    lpart_names = ["Pi", "K"]
    lpart_titles = ["#pi", "K"]
    ldca_names = ["a", "b"]
    ldca_titles = ["{xy}", "{z}"]

    canvas = TCanvas("cpik_dca")
    canvas.Divide(2, 2)

    label = TPaveText(0.6, 0.75, 0.8, 0.85, "NDC")
    label.AddText(run)
    label.SetTextSize(0.05)
    label.SetFillColor(0)
    label.SetFillColor(0)
    label.SetBorderSize(0)

    llegends = []
    for _ in range(4):
        legend = TLegend(0.6, 0.55, 0.8, 0.75)
        legend.SetLineWidth(0)
        legend.SetTextSize(0.05)
        llegends.append(legend)
    
    ltextboxes = []
    for _ in range(2):
        textbox = TPaveText(0.25, 0.5, 0.5, 0.85, "NDC")
        textbox.AddText("Percentage of events")
        textbox.SetTextSize(0.04)
        textbox.SetFillColor(0)
        textbox.SetFillColor(0)
        textbox.SetBorderSize(0)
        ltextboxes.append(textbox)
    
    lbkg_clones = [None] * 4
    lsig_clones = [None] * 4
    
    pad = 0
    for i in range(2):      # loop over particle types
        for j in range(2):      # loop over DCA types
            histname_bkg = "hRcPrim{}Loc{}ToRCVtx".format(lpart_names[i], ldca_names[j])
            histname_sig = "hRcSec{}Loc{}ToRCVtx".format(lpart_names[i], ldca_names[j])

            hbkg = infile.Get(histname_bkg)
            hsig = infile.Get(histname_sig)

            proj_bkg = hbkg.ProjectionZ(histname_bkg+"_projDca")
            proj_bkg.Scale(1 / proj_bkg.Integral())
            proj_bkg.GetYaxis().SetTitle("Normalized events")
            proj_sig = hsig.ProjectionZ(histname_sig+"_proj")
            proj_sig.Scale(1 / proj_sig.Integral())
            proj_sig.GetYaxis().SetTitle("Normalized events")

            ymax = max([proj_bkg.GetMaximum(), proj_sig.GetMaximum()])
            
            canvas.cd(pad+1)
            lbkg_clones[pad] = proj_bkg.Clone(histname_bkg+"_clone")
            lbkg_clones[pad].SetMaximum(1.2 * ymax)
            lbkg_clones[pad].SetTitle(
                "DCA_{} of {} decay and secondary {}".format(ldca_titles[j], "D^{0}", lpart_titles[i])
            )
            lsig_clones[pad] = proj_sig.Clone(histname_sig+"_clone")

            lbkg_clones[pad].SetLineStyle(1)        # solid line
            lbkg_clones[pad].SetLineColor(kRed)
            lbkg_clones[pad].SetStats(0)

            lsig_clones[pad].SetMarkerStyle(20)     # circle
            lsig_clones[pad].SetMarkerSize(0.5)
            lsig_clones[pad].SetLineColor(kBlack)
            lsig_clones[pad].SetMarkerColor(kBlack)

            lbkg_clones[pad].Draw("hist")
            lsig_clones[pad].Draw("p same")
            lsig_clones[pad].Draw("e0 same")
            
            llegends[pad].AddEntry(lsig_clones[pad], "{} decayed {}".format("D^{0}", lpart_titles[i]), "lp")
            llegends[pad].AddEntry(lbkg_clones[pad], "Primary {}".format(lpart_titles[i]), "l")
            llegends[pad].Draw()

            label.Draw()

            # Calculate percentage of events for DCA_xy < 0.05, 0.1, 0.15.
            if j == 0:
                for dca_xy_cut in [0.05, 0.1, 0.15]:
                    bin = proj_bkg.FindBin(dca_xy_cut) - 1
                    bin_edge = proj_bkg.GetXaxis().GetBinUpEdge(bin)
                    bkg_ratio = proj_bkg.Integral(1, bin) / proj_bkg.Integral()
                    sig_ratio = proj_sig.Integral(1, bin) / proj_sig.Integral()

                    bkg_text = f"{bkg_ratio:.2f}"
                    sig_text = f"{sig_ratio:.2f}"
                    
                    ltextboxes[i].AddText("{} < {} : {}, #color[2]{}".format(
                        "DCA_{xy}", bin_edge, sig_text, {bkg_text}))
                ltextboxes[i].Draw()

            pad += 1
    
    canvas.Print("h{}_scaled_piK_DCA_proj.pdf".format(run))
    print("--- Projections done: ({}) DCA of pi/K".format(run))

def decay_topo_proj(infile, run):
    """
    Plot DCA_12, cos(theta), DCA, decay length of signal and bkg pi+K pairs.
    Projected from 3D histograms of (variable) vs. pT and eta.
    
    Args:
    infile (TFile): root file containing 3D histograms
    run (str): identifying name of the simulation run

    Outputs:
    Prints pdf of canvas containing plots.
    Returns: None
    """
    lvar_names = ["Dca12", "CosTheta", "Dca", "DecayLength"]
    lvar_titles = ["DCA_{12}", "cos(#theta)", "DCA", "decay length"]
    
    canvas = TCanvas("cpair_decay")
    canvas.Divide(2, 2)

    label = TPaveText(0.6, 0.75, 0.8, 0.85, "NDC")
    label.AddText(run)
    label.SetTextSize(0.05)
    label.SetFillColor(0)
    label.SetFillColor(0)
    label.SetBorderSize(0)

    llegends = []
    for _ in range(4):
        legend = TLegend(0.6, 0.55, 0.8, 0.75)
        legend.SetLineWidth(0)
        legend.SetTextSize(0.05)
        llegends.append(legend)
    
    lbkg_clones = [None] * 4
    lsig_clones = [None] * 4

    for i in range(4):
        histname_bkg = "h3Pair{}_bkg".format(lvar_names[i])
        histname_sig = "h3Pair{}_signal".format(lvar_names[i])

        hbkg = infile.Get(histname_bkg)
        hsig = infile.Get(histname_sig)

        proj_bkg = hbkg.ProjectionZ(histname_bkg+"_proj")
        proj_bkg.Scale(1 / proj_bkg.Integral())
        proj_bkg.GetYaxis().SetTitle("Normalized events")
        proj_sig = hsig.ProjectionZ(histname_sig+"_proj")
        proj_sig.Scale(1 / proj_sig.Integral())
        proj_sig.GetYaxis().SetTitle("Normalized events")

        ymax = max([proj_bkg.GetMaximum(), proj_sig.GetMaximum()])

        canvas.cd(i+1)
        lbkg_clones[i] = proj_bkg.Clone(histname_bkg+"_clone")
        lbkg_clones[i].SetMaximum(1.2 * ymax)
        lbkg_clones[i].SetTitle(
            "Pair {} signal and background".format(lvar_titles[i])
        )
        lsig_clones[i] = proj_sig.Clone(histname_sig+"_clone")

        lbkg_clones[i].SetLineStyle(1)        # solid line
        # lbkg_clones[i].SetFillStyle(1001)     # solid fill
        lbkg_clones[i].SetLineColor(kRed)
        # lbkg_clones[i].SetFillColor(kOrange)
        lbkg_clones[i].SetStats(0)

        lsig_clones[i].SetMarkerStyle(20)     # circle
        lsig_clones[i].SetMarkerSize(0.5)
        lsig_clones[i].SetLineColor(kBlack)
        lsig_clones[i].SetMarkerColor(kBlack)

        lbkg_clones[i].Draw("hist")
        lsig_clones[i].Draw("p same")
        lsig_clones[i].Draw("e0 same")
        
        llegends[i].AddEntry(lsig_clones[i], "Signal", "lp")
        llegends[i].AddEntry(lbkg_clones[i], "Background", "l")
        llegends[i].Draw()

        label.Draw()
        
    canvas.Print("h{}_scaled_decay_topo_proj.pdf".format(run))
    print("--- Projections done: ({}) decay topology".format(run))

def inv_mass_proj(infile, run):
    """
    Plot invariant mass of pi+K pairs for signal and bkg events, with and
    without DCA cuts. Projected from 3D histograms of inv mass vs. pT and eta.
    
    Args:
    infile (TFile): root file containing 3D histograms
    run (str): identifying name of the simulation run

    Outputs:
    Prints pdf of canvas containing plots.
    Returns: None
    """
    lcut_names = ["all", "DCA"]
    lcut_titles = ["all", "after DCA cuts"]

    canvas = TCanvas("cpair_inv_mass")
    canvas.Divide(1, 2)

    label = TPaveText(0.7, 0.75, 0.8, 0.85, "NDC")
    label.AddText(run)
    label.SetTextSize(0.07)
    label.SetFillColor(0)
    label.SetFillColor(0)
    label.SetBorderSize(0)

    llegends = []
    for _ in range(2):
        legend = TLegend(0.7, 0.55, 0.8, 0.7)
        legend.SetLineWidth(0)
        legend.SetTextSize(0.05)
        llegends.append(legend)
    
    lbkg_clones = [None] * 2
    lsig_clones = [None] * 2
    

    for i in range(2):
        histname_bkg = "h3InvMass_bkg_{}".format(lcut_names[i])
        histname_sig = "h3InvMass_signal_{}".format(lcut_names[i])

        hbkg = infile.Get(histname_bkg)
        hsig = infile.Get(histname_sig)

        proj_bkg = hbkg.ProjectionZ(histname_bkg+"_projZ")
        # proj_bkg.Scale(1 / proj_bkg.Integral())
        proj_bkg.GetYaxis().SetTitle("Absolute number of events")
        proj_sig = hsig.ProjectionZ(histname_sig+"_projZ")
        # proj_sig.Scale(1 / proj_sig.Integral())
        proj_sig.GetYaxis().SetTitle("Absolute number of events")

        ymax = max([proj_bkg.GetMaximum(), proj_sig.GetMaximum()])

        canvas.cd(i+1)
        lbkg_clones[i] = proj_bkg.Clone(histname_bkg+"_clone")
        lbkg_clones[i].SetMaximum(1.2 * ymax)
        lbkg_clones[i].SetTitle(
            "Invariant mass of unlike-sign #piK pairs ({})".format(lcut_titles[i])
        )
        lsig_clones[i] = proj_sig.Clone(histname_sig+"_clone")

        lbkg_clones[i].SetLineStyle(1)        # solid line
        # lbkg_clones[i].SetFillStyle(1001)     # solid fill
        lbkg_clones[i].SetLineColor(kRed)
        # lbkg_clones[i].SetFillColor(kOrange)
        lbkg_clones[i].SetStats(0)

        lsig_clones[i].SetMarkerStyle(20)     # circle
        lsig_clones[i].SetMarkerSize(0.5)
        lsig_clones[i].SetLineColor(kBlack)
        lsig_clones[i].SetMarkerColor(kBlack)

        lbkg_clones[i].Draw("hist")
        lsig_clones[i].Draw("p same")
        lsig_clones[i].Draw("e0 same")
        
        llegends[i].SetLineWidth(0)
        llegends[i].SetTextSize(0.07)
        llegends[i].AddEntry(lsig_clones[i], "Signal", "lp")
        llegends[i].AddEntry(lbkg_clones[i], "Background", "l")
        llegends[i].Draw()

        label.Draw()
    
    canvas.Print("h{}_inv_mass_proj.pdf".format(run))
    print("--- Projections done: ({}) invariant mass".format(run))

def pik_pt_eta_proj(infile, run):
    """
    Plot pt and eta of D0-decayed (secondary) and bkg (primary)
    pions and kaons. Projected from 3D histograms of DCA vs. pT and eta.
    
    Args:
    infile (TFile): root file containing 3D histograms
    run (str): identifying name of the simulation run

    Outputs:
    Prints pdf of canvas containing plots.
    Returns: None
    """
    lpart_names = ["Pi", "K"]
    lpart_titles = ["#pi", "K"]
    lvar_titles = ["p_{T}", "#eta"]

    canvas = TCanvas("cpik_pt_eta")
    canvas.Divide(2, 2)

    label1 = TPaveText(0.6, 0.75, 0.8, 0.85, "NDC")
    label2 = TPaveText(0.2, 0.75, 0.4, 0.85, "NDC")
    llabels = [label1, label2]
    for label in llabels:
        label.AddText(run)
        label.SetTextSize(0.05)
        label.SetFillColor(0)
        label.SetFillColor(0)
        label.SetBorderSize(0)

    llegends = []
    for _ in range(2):
        legend1 = TLegend(0.6, 0.55, 0.8, 0.75)
        legend1.SetLineWidth(0)
        legend1.SetTextSize(0.05)
        llegends.append(legend1)

        legend2 = TLegend(0.15, 0.55, 0.35, 0.75)
        legend2.SetLineWidth(0)
        legend2.SetTextSize(0.05)
        llegends.append(legend2)
    
    
    lbkg_clones = [None] * 4
    lsig_clones = [None] * 4

    pad = 0
    for i in range(2):      # loop over particle types
        for j in range(2):      # loop over variable types (pt, eta)
            histname_bkg = "hRcPrim{}LocaToRCVtx".format(lpart_names[i])
            histname_sig = "hRcSec{}LocaToRCVtx".format(lpart_names[i])

            hbkg = infile.Get(histname_bkg)
            hsig = infile.Get(histname_sig)

            if j == 0:
                proj_bkg = hbkg.ProjectionX(histname_bkg+"_projPt")
                proj_sig = hsig.ProjectionX(histname_sig+"_projPt")
            else:
                proj_bkg = hbkg.ProjectionY(histname_bkg+"_projEta")
                proj_sig = hsig.ProjectionY(histname_sig+"_projEta")

            proj_bkg.Scale(1 / proj_bkg.Integral())
            proj_bkg.GetYaxis().SetTitle("Normalized events")
            proj_sig.Scale(1 / proj_sig.Integral())
            proj_sig.GetYaxis().SetTitle("Normalized events")

            ymax = max([proj_bkg.GetMaximum(), proj_sig.GetMaximum()])
            
            canvas.cd(pad+1)
            lbkg_clones[pad] = proj_bkg.Clone(histname_bkg+"_clone")
            lbkg_clones[pad].SetMaximum(1.2 * ymax)
            lbkg_clones[pad].SetTitle(
                "{} of {} decay and secondary {}".format(lvar_titles[j], "D^{0}", lpart_titles[i])
            )
            lsig_clones[pad] = proj_sig.Clone(histname_sig+"_clone")

            lbkg_clones[pad].SetLineStyle(1)        # solid line
            lbkg_clones[pad].SetLineColor(kRed)
            lbkg_clones[pad].SetStats(0)

            lsig_clones[pad].SetMarkerStyle(20)     # circle
            lsig_clones[pad].SetMarkerSize(0.5)
            lsig_clones[pad].SetLineColor(kBlack)
            lsig_clones[pad].SetMarkerColor(kBlack)

            lbkg_clones[pad].Draw("hist")
            lsig_clones[pad].Draw("p same")
            lsig_clones[pad].Draw("e0 same")

            llegends[pad].AddEntry(lsig_clones[pad], "{} decayed {}".format("D^{0}", lpart_titles[i]), "lp")
            llegends[pad].AddEntry(lbkg_clones[pad], "Primary {}".format(lpart_titles[i]), "l")
            llegends[pad].Draw()

            llabels[j].Draw()

            pad += 1
    
    canvas.Print("h{}_scaled_piK_pteta_proj.pdf".format(run))
    print("--- Projections done: ({}) pt and eta of pi/K".format(run))

def pair_pt_rap_proj(infile, run):
    """
    Plot pt and rapidity (y) of pi+K pairs for signal and bkg events, with and
    without DCA cuts. Projected from 3D histograms of inv mass vs. pT and eta.
    
    Args:
    infile (TFile): root file containing 3D histograms
    run (str): identifying name of the simulation run

    Outputs:
    Prints pdf of canvas containing plots.
    Returns: None
    """
    lcut_names = ["all", "DCA"]
    lcut_titles = ["all", "after DCA cuts"]
    lvar_titles = ["p_{T}", "Rapidity"]

    canvas = TCanvas("cpair_pt_eta")
    canvas.Divide(2, 2)

    label1 = TPaveText(0.6, 0.75, 0.8, 0.85, "NDC")
    label2 = TPaveText(0.2, 0.75, 0.4, 0.85, "NDC")
    llabels = [label1, label2]
    for label in llabels:
        label.AddText(run)
        label.SetTextSize(0.05)
        label.SetFillColor(0)
        label.SetFillColor(0)
        label.SetBorderSize(0)

    llegends = []
    for _ in range(2):
        legend1 = TLegend(0.6, 0.55, 0.8, 0.75)
        legend1.SetLineWidth(0)
        legend1.SetTextSize(0.05)
        llegends.append(legend1)

        legend2 = TLegend(0.15, 0.55, 0.35, 0.75)
        legend2.SetLineWidth(0)
        legend2.SetTextSize(0.05)
        llegends.append(legend2)
    
    lbkg_clones = [None] * 4
    lsig_clones = [None] * 4

    pad = 0
    for i in range(2):  # loop over cut types
        for j in range(2):  # loop over variable types (pt, eta)
            histname_bkg = "h3InvMass_bkg_{}".format(lcut_names[i])
            histname_sig = "h3InvMass_signal_{}".format(lcut_names[i])

            hbkg = infile.Get(histname_bkg)
            hsig = infile.Get(histname_sig)

            if j == 0:
                proj_bkg = hbkg.ProjectionX(histname_bkg+"_projPt")
                proj_sig = hsig.ProjectionX(histname_sig+"_projPt")
            else:
                proj_bkg = hbkg.ProjectionY(histname_bkg+"_projRap")
                proj_sig = hsig.ProjectionY(histname_sig+"_projRap")

            proj_bkg.Scale(1 / proj_bkg.Integral())
            proj_bkg.GetYaxis().SetTitle("Normalized events")
            proj_sig.Scale(1 / proj_sig.Integral())
            proj_sig.GetYaxis().SetTitle("Normalized events")

            ymax = max([proj_bkg.GetMaximum(), proj_sig.GetMaximum()])

            canvas.cd(pad+1)
            lbkg_clones[pad] = proj_bkg.Clone(histname_bkg+"_clone")
            lbkg_clones[pad].SetMaximum(1.2 * ymax)
            lbkg_clones[pad].SetTitle(
                "{} of unlike-sign #piK pairs ({})".format(lvar_titles[j], lcut_titles[i])
            )
            lsig_clones[pad] = proj_sig.Clone(histname_sig+"_clone")

            lbkg_clones[pad].SetLineStyle(1)        # solid line
            lbkg_clones[pad].SetLineColor(kRed)
            lbkg_clones[pad].SetStats(0)

            lsig_clones[pad].SetMarkerStyle(20)     # circle
            lsig_clones[pad].SetMarkerSize(0.5)
            lsig_clones[pad].SetLineColor(kBlack)
            lsig_clones[pad].SetMarkerColor(kBlack)

            lbkg_clones[pad].Draw("hist")
            lsig_clones[pad].Draw("p same")
            lsig_clones[pad].Draw("e0 same")
            
            llegends[pad].SetLineWidth(0)
            llegends[pad].SetTextSize(0.07)
            llegends[pad].AddEntry(lsig_clones[i], "Signal", "lp")
            llegends[pad].AddEntry(lbkg_clones[i], "Background", "l")
            llegends[pad].Draw()

            llabels[j].Draw()

            pad += 1
    
    canvas.Print("h{}_scaled_pair_ptrap_proj.pdf".format(run))
    print("--- Projections done: ({}) pair pt and rapidity".format(run))



def main():
    run = "q2_1_run10_0187"   # q2_100_run10_0186, q2_1_run10_0187
    infile = TFile("/home/cy2306/eic/vertexing_D0/ePIC/HF_reco/helix/q2_1_run10_0187.root", "READ")
    outfile = TFile.Open("r{}_sig_vs_bkg_proj.root".format(run), "RECREATE")

    # pik_dca_proj(infile, run)         # DCA of pi/K
    # decay_topo_proj(infile, run)      # pair decay topology
    # inv_mass_proj(infile, run)        # pair invariant mass

    # pik_pt_eta_proj(infile, run)      # pt and eta of pi/K
    pair_pt_rap_proj(infile, run)     # pt and eta of pair


    # outfile.Write()
    # outfile.Close()

if __name__ == "__main__":
    main()