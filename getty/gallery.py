import config
from analysis.inspector import getty_csi_init, getty_csi_targets_prep
from tools.git import git_commit_msgs, github_info
from tools.hdiff import diff_to_html, getty_append_semainfo, srcdiff2html
from tools.os import sys_call


def _l2m_correction(l2m, rts):
    result = {}
    for file_line_key in l2m:
        candidate_map = {}
        simple_info = l2m[file_line_key]
        last_dash = simple_info.rfind("-")
        if last_dash != -1:
            for t in rts:
                lp = t.find("(")
                if lp != -1 and t[:lp] == simple_info[:last_dash]:
                    dash_pos = t.rfind("-")
                    if dash_pos != -1:
                        ln = int(t[dash_pos+1:])
                        candidate_map[ln] = t
            ori = int(simple_info[last_dash+1:])
            correct = None
            for aln in sorted(candidate_map.keys()):
                if ori < aln:
                    correct = aln
                    break
            if correct is not None:
                result[file_line_key] = candidate_map[correct]
    return result


def exam(iso, pwd, go, fe_path, common_package, all_classes_set,
         targets, all_refined_target_set,
         new_refined_target_set, old_refined_target_set,
         all_changed_methods, new_changed_methods, old_changed_methods,
         new_modified_src, new_all_src,
         new_caller_of, new_callee_of, new_pred_of, new_succ_of,
         old_caller_of, old_callee_of, old_pred_of, old_succ_of,
         all_changed_tests, old_changed_tests, new_changed_tests,
         old_test_set, new_test_set,
         prev_hash, post_hash, old_l2m, new_l2m, old_m2l, new_m2l):
    
    # TODO: NEEDS BETTER REFINED TARGET SETS
    refined_targets_parents_set = all_refined_target_set | all_classes_set
    
    print 'generating full diff html ...'
    # get extra diff file for full diff of each changed file
    full_src_diff_in = go + "full.text.diff"
    full_src_diff_out = go + "src.diff.html"
    sys_call(
        " ".join(["git diff",
                  "--unified={3}", str(config.git_diff_extra_ops),
                  "{0} {1} > {2}"]).format(
            prev_hash, post_hash, full_src_diff_in, config.max_context_line))
    
    # correct old_l2m and new_l2m
    old_l2m = _l2m_correction(old_l2m, old_refined_target_set)
    new_l2m = _l2m_correction(new_l2m, new_refined_target_set)
    
    srcdiff2html(
        full_src_diff_in, full_src_diff_out,
        exclude_headers=None, old_l2m=old_l2m, new_l2m=new_l2m)
    
    print 'generating main html from diff ...'
    diff_in = go + "text.diff"
    html_out = go + "sema.diff.html"    
    diff_to_html(diff_in, html_out,
        exclude_headers=False, old_l2m=old_l2m, new_l2m=new_l2m)
    
    print 'appending semainfo to the html ....'
    commit_msgs = git_commit_msgs(prev_hash, post_hash)
    github_link = github_info(prev_hash, post_hash)
    getty_append_semainfo(html_out, refined_targets_parents_set, go, fe_path,
                          commit_msgs, github_link,
                          prev_hash, post_hash, old_l2m, new_l2m, iso)
    
    print 'initialize csi report ...'
    getty_csi_init(html_out, iso)
    
    print 'setting csi target variables ...'
    getty_csi_targets_prep(
        html_out, go, prev_hash, post_hash, common_package,
        all_changed_tests, old_changed_tests, new_changed_tests,
        all_changed_methods, new_modified_src, new_all_src,
        old_test_set, new_test_set,
        old_caller_of, old_callee_of, old_pred_of, old_succ_of,
        new_caller_of, new_callee_of, new_pred_of, new_succ_of,
        old_refined_target_set, new_refined_target_set, all_refined_target_set,
        all_classes_set, iso,
        expansion_set=refined_targets_parents_set)  # TODO: which expanded set to use?
    
    print 'csi report page is set.'
    
    if config.review_auto_open:
        print '  Opening rendered pages for review ...'
        sys_call("open " + html_out)
    else:
        print '  CSI analysis completed - review at: ' + html_out
