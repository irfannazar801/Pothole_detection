# 🐛 Bug Fix - Unpacking Error Resolved

## Issue

When running the application, it crashed with this error:
```
ValueError: too many values to unpack (expected 2)
  File "severity_estimator.py", line 281, in estimate_muddy_pothole_depth
    label, color = self._classify_severity(depth_cm, "MUD")
```

## Root Cause

The `_classify_severity()` method returns **3 values**:
```python
return label, level.value[1], depth_cm  # Returns (label, color, depth)
```

But `estimate_muddy_pothole_depth()` was only unpacking **2 values**:
```python
label, color = self._classify_severity(depth_cm, "MUD")  # ❌ Only 2 variables
```

## Fix Applied

Updated the unpacking to handle all 3 return values:

**Before:**
```python
label, color = self._classify_severity(depth_cm, "MUD")
```

**After:**
```python
label, color, _ = self._classify_severity(depth_cm, "MUD")  # ✅ Unpack 3 values
```

## Files Modified

1. **`src/severity_estimator.py`** - Line 281
   - Fixed unpacking from 2 to 3 values
   - Added underscore `_` to ignore the depth value (not needed in muddy pothole estimation)

2. **`run.py`** - Line 8
   - Updated example usage to use correct video path: `videos/demo.mp4`

## Testing

The application should now work correctly:

```bash
# This should now work without errors
python run.py --video videos/demo.mp4

# Or with default config
python run.py
```

## Status

✅ **Bug Fixed**  
✅ **Code Updated**  
✅ **Ready to Run**

---

**Fixed**: January 21, 2026  
**Type**: ValueError - Unpacking Error  
**Severity**: Critical (app crash)  
**Status**: ✅ Resolved
