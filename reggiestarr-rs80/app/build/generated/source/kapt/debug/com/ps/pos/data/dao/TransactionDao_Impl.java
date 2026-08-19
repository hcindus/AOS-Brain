package com.ps.pos.data.dao;

import android.database.Cursor;
import android.os.CancellationSignal;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.room.CoroutinesRoom;
import androidx.room.EntityInsertionAdapter;
import androidx.room.RoomDatabase;
import androidx.room.RoomSQLiteQuery;
import androidx.room.SharedSQLiteStatement;
import androidx.room.util.CursorUtil;
import androidx.room.util.DBUtil;
import androidx.sqlite.db.SupportSQLiteStatement;
import com.ps.pos.data.entities.Transaction;
import java.lang.Class;
import java.lang.Double;
import java.lang.Exception;
import java.lang.Long;
import java.lang.Object;
import java.lang.Override;
import java.lang.String;
import java.lang.SuppressWarnings;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.Callable;
import javax.annotation.processing.Generated;
import kotlin.Unit;
import kotlin.coroutines.Continuation;
import kotlinx.coroutines.flow.Flow;

@Generated("androidx.room.RoomProcessor")
@SuppressWarnings({"unchecked", "deprecation"})
public final class TransactionDao_Impl implements TransactionDao {
  private final RoomDatabase __db;

  private final EntityInsertionAdapter<Transaction> __insertionAdapterOfTransaction;

  private final SharedSQLiteStatement __preparedStmtOfVoidTransaction;

  public TransactionDao_Impl(@NonNull final RoomDatabase __db) {
    this.__db = __db;
    this.__insertionAdapterOfTransaction = new EntityInsertionAdapter<Transaction>(__db) {
      @Override
      @NonNull
      protected String createQuery() {
        return "INSERT OR REPLACE INTO `transactions` (`id`,`transactionNumber`,`timestamp`,`subtotal`,`tax`,`total`,`paymentType`,`tendered`,`change`,`status`) VALUES (nullif(?, 0),?,?,?,?,?,?,?,?,?)";
      }

      @Override
      protected void bind(@NonNull final SupportSQLiteStatement statement,
          @NonNull final Transaction entity) {
        statement.bindLong(1, entity.getId());
        if (entity.getTransactionNumber() == null) {
          statement.bindNull(2);
        } else {
          statement.bindString(2, entity.getTransactionNumber());
        }
        statement.bindLong(3, entity.getTimestamp());
        statement.bindDouble(4, entity.getSubtotal());
        statement.bindDouble(5, entity.getTax());
        statement.bindDouble(6, entity.getTotal());
        if (entity.getPaymentType() == null) {
          statement.bindNull(7);
        } else {
          statement.bindString(7, entity.getPaymentType());
        }
        statement.bindDouble(8, entity.getTendered());
        statement.bindDouble(9, entity.getChange());
        if (entity.getStatus() == null) {
          statement.bindNull(10);
        } else {
          statement.bindString(10, entity.getStatus());
        }
      }
    };
    this.__preparedStmtOfVoidTransaction = new SharedSQLiteStatement(__db) {
      @Override
      @NonNull
      public String createQuery() {
        final String _query = "UPDATE transactions SET status = 'VOIDED' WHERE id = ?";
        return _query;
      }
    };
  }

  @Override
  public Object insert(final Transaction transaction,
      final Continuation<? super Long> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Long>() {
      @Override
      @NonNull
      public Long call() throws Exception {
        __db.beginTransaction();
        try {
          final Long _result = __insertionAdapterOfTransaction.insertAndReturnId(transaction);
          __db.setTransactionSuccessful();
          return _result;
        } finally {
          __db.endTransaction();
        }
      }
    }, $completion);
  }

  @Override
  public Object voidTransaction(final long id, final Continuation<? super Unit> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Unit>() {
      @Override
      @NonNull
      public Unit call() throws Exception {
        final SupportSQLiteStatement _stmt = __preparedStmtOfVoidTransaction.acquire();
        int _argIndex = 1;
        _stmt.bindLong(_argIndex, id);
        try {
          __db.beginTransaction();
          try {
            _stmt.executeUpdateDelete();
            __db.setTransactionSuccessful();
            return Unit.INSTANCE;
          } finally {
            __db.endTransaction();
          }
        } finally {
          __preparedStmtOfVoidTransaction.release(_stmt);
        }
      }
    }, $completion);
  }

  @Override
  public Flow<List<Transaction>> getAllTransactions() {
    final String _sql = "SELECT * FROM transactions ORDER BY timestamp DESC";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 0);
    return CoroutinesRoom.createFlow(__db, false, new String[] {"transactions"}, new Callable<List<Transaction>>() {
      @Override
      @NonNull
      public List<Transaction> call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfId = CursorUtil.getColumnIndexOrThrow(_cursor, "id");
          final int _cursorIndexOfTransactionNumber = CursorUtil.getColumnIndexOrThrow(_cursor, "transactionNumber");
          final int _cursorIndexOfTimestamp = CursorUtil.getColumnIndexOrThrow(_cursor, "timestamp");
          final int _cursorIndexOfSubtotal = CursorUtil.getColumnIndexOrThrow(_cursor, "subtotal");
          final int _cursorIndexOfTax = CursorUtil.getColumnIndexOrThrow(_cursor, "tax");
          final int _cursorIndexOfTotal = CursorUtil.getColumnIndexOrThrow(_cursor, "total");
          final int _cursorIndexOfPaymentType = CursorUtil.getColumnIndexOrThrow(_cursor, "paymentType");
          final int _cursorIndexOfTendered = CursorUtil.getColumnIndexOrThrow(_cursor, "tendered");
          final int _cursorIndexOfChange = CursorUtil.getColumnIndexOrThrow(_cursor, "change");
          final int _cursorIndexOfStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "status");
          final List<Transaction> _result = new ArrayList<Transaction>(_cursor.getCount());
          while (_cursor.moveToNext()) {
            final Transaction _item;
            final long _tmpId;
            _tmpId = _cursor.getLong(_cursorIndexOfId);
            final String _tmpTransactionNumber;
            if (_cursor.isNull(_cursorIndexOfTransactionNumber)) {
              _tmpTransactionNumber = null;
            } else {
              _tmpTransactionNumber = _cursor.getString(_cursorIndexOfTransactionNumber);
            }
            final long _tmpTimestamp;
            _tmpTimestamp = _cursor.getLong(_cursorIndexOfTimestamp);
            final double _tmpSubtotal;
            _tmpSubtotal = _cursor.getDouble(_cursorIndexOfSubtotal);
            final double _tmpTax;
            _tmpTax = _cursor.getDouble(_cursorIndexOfTax);
            final double _tmpTotal;
            _tmpTotal = _cursor.getDouble(_cursorIndexOfTotal);
            final String _tmpPaymentType;
            if (_cursor.isNull(_cursorIndexOfPaymentType)) {
              _tmpPaymentType = null;
            } else {
              _tmpPaymentType = _cursor.getString(_cursorIndexOfPaymentType);
            }
            final double _tmpTendered;
            _tmpTendered = _cursor.getDouble(_cursorIndexOfTendered);
            final double _tmpChange;
            _tmpChange = _cursor.getDouble(_cursorIndexOfChange);
            final String _tmpStatus;
            if (_cursor.isNull(_cursorIndexOfStatus)) {
              _tmpStatus = null;
            } else {
              _tmpStatus = _cursor.getString(_cursorIndexOfStatus);
            }
            _item = new Transaction(_tmpId,_tmpTransactionNumber,_tmpTimestamp,_tmpSubtotal,_tmpTax,_tmpTotal,_tmpPaymentType,_tmpTendered,_tmpChange,_tmpStatus);
            _result.add(_item);
          }
          return _result;
        } finally {
          _cursor.close();
        }
      }

      @Override
      protected void finalize() {
        _statement.release();
      }
    });
  }

  @Override
  public Object getById(final long id, final Continuation<? super Transaction> $completion) {
    final String _sql = "SELECT * FROM transactions WHERE id = ? LIMIT 1";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 1);
    int _argIndex = 1;
    _statement.bindLong(_argIndex, id);
    final CancellationSignal _cancellationSignal = DBUtil.createCancellationSignal();
    return CoroutinesRoom.execute(__db, false, _cancellationSignal, new Callable<Transaction>() {
      @Override
      @Nullable
      public Transaction call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfId = CursorUtil.getColumnIndexOrThrow(_cursor, "id");
          final int _cursorIndexOfTransactionNumber = CursorUtil.getColumnIndexOrThrow(_cursor, "transactionNumber");
          final int _cursorIndexOfTimestamp = CursorUtil.getColumnIndexOrThrow(_cursor, "timestamp");
          final int _cursorIndexOfSubtotal = CursorUtil.getColumnIndexOrThrow(_cursor, "subtotal");
          final int _cursorIndexOfTax = CursorUtil.getColumnIndexOrThrow(_cursor, "tax");
          final int _cursorIndexOfTotal = CursorUtil.getColumnIndexOrThrow(_cursor, "total");
          final int _cursorIndexOfPaymentType = CursorUtil.getColumnIndexOrThrow(_cursor, "paymentType");
          final int _cursorIndexOfTendered = CursorUtil.getColumnIndexOrThrow(_cursor, "tendered");
          final int _cursorIndexOfChange = CursorUtil.getColumnIndexOrThrow(_cursor, "change");
          final int _cursorIndexOfStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "status");
          final Transaction _result;
          if (_cursor.moveToFirst()) {
            final long _tmpId;
            _tmpId = _cursor.getLong(_cursorIndexOfId);
            final String _tmpTransactionNumber;
            if (_cursor.isNull(_cursorIndexOfTransactionNumber)) {
              _tmpTransactionNumber = null;
            } else {
              _tmpTransactionNumber = _cursor.getString(_cursorIndexOfTransactionNumber);
            }
            final long _tmpTimestamp;
            _tmpTimestamp = _cursor.getLong(_cursorIndexOfTimestamp);
            final double _tmpSubtotal;
            _tmpSubtotal = _cursor.getDouble(_cursorIndexOfSubtotal);
            final double _tmpTax;
            _tmpTax = _cursor.getDouble(_cursorIndexOfTax);
            final double _tmpTotal;
            _tmpTotal = _cursor.getDouble(_cursorIndexOfTotal);
            final String _tmpPaymentType;
            if (_cursor.isNull(_cursorIndexOfPaymentType)) {
              _tmpPaymentType = null;
            } else {
              _tmpPaymentType = _cursor.getString(_cursorIndexOfPaymentType);
            }
            final double _tmpTendered;
            _tmpTendered = _cursor.getDouble(_cursorIndexOfTendered);
            final double _tmpChange;
            _tmpChange = _cursor.getDouble(_cursorIndexOfChange);
            final String _tmpStatus;
            if (_cursor.isNull(_cursorIndexOfStatus)) {
              _tmpStatus = null;
            } else {
              _tmpStatus = _cursor.getString(_cursorIndexOfStatus);
            }
            _result = new Transaction(_tmpId,_tmpTransactionNumber,_tmpTimestamp,_tmpSubtotal,_tmpTax,_tmpTotal,_tmpPaymentType,_tmpTendered,_tmpChange,_tmpStatus);
          } else {
            _result = null;
          }
          return _result;
        } finally {
          _cursor.close();
          _statement.release();
        }
      }
    }, $completion);
  }

  @Override
  public Flow<List<Transaction>> getTodayTransactions() {
    final String _sql = "SELECT * FROM transactions WHERE date(timestamp/1000, 'unixepoch') = date('now') ORDER BY timestamp DESC";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 0);
    return CoroutinesRoom.createFlow(__db, false, new String[] {"transactions"}, new Callable<List<Transaction>>() {
      @Override
      @NonNull
      public List<Transaction> call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfId = CursorUtil.getColumnIndexOrThrow(_cursor, "id");
          final int _cursorIndexOfTransactionNumber = CursorUtil.getColumnIndexOrThrow(_cursor, "transactionNumber");
          final int _cursorIndexOfTimestamp = CursorUtil.getColumnIndexOrThrow(_cursor, "timestamp");
          final int _cursorIndexOfSubtotal = CursorUtil.getColumnIndexOrThrow(_cursor, "subtotal");
          final int _cursorIndexOfTax = CursorUtil.getColumnIndexOrThrow(_cursor, "tax");
          final int _cursorIndexOfTotal = CursorUtil.getColumnIndexOrThrow(_cursor, "total");
          final int _cursorIndexOfPaymentType = CursorUtil.getColumnIndexOrThrow(_cursor, "paymentType");
          final int _cursorIndexOfTendered = CursorUtil.getColumnIndexOrThrow(_cursor, "tendered");
          final int _cursorIndexOfChange = CursorUtil.getColumnIndexOrThrow(_cursor, "change");
          final int _cursorIndexOfStatus = CursorUtil.getColumnIndexOrThrow(_cursor, "status");
          final List<Transaction> _result = new ArrayList<Transaction>(_cursor.getCount());
          while (_cursor.moveToNext()) {
            final Transaction _item;
            final long _tmpId;
            _tmpId = _cursor.getLong(_cursorIndexOfId);
            final String _tmpTransactionNumber;
            if (_cursor.isNull(_cursorIndexOfTransactionNumber)) {
              _tmpTransactionNumber = null;
            } else {
              _tmpTransactionNumber = _cursor.getString(_cursorIndexOfTransactionNumber);
            }
            final long _tmpTimestamp;
            _tmpTimestamp = _cursor.getLong(_cursorIndexOfTimestamp);
            final double _tmpSubtotal;
            _tmpSubtotal = _cursor.getDouble(_cursorIndexOfSubtotal);
            final double _tmpTax;
            _tmpTax = _cursor.getDouble(_cursorIndexOfTax);
            final double _tmpTotal;
            _tmpTotal = _cursor.getDouble(_cursorIndexOfTotal);
            final String _tmpPaymentType;
            if (_cursor.isNull(_cursorIndexOfPaymentType)) {
              _tmpPaymentType = null;
            } else {
              _tmpPaymentType = _cursor.getString(_cursorIndexOfPaymentType);
            }
            final double _tmpTendered;
            _tmpTendered = _cursor.getDouble(_cursorIndexOfTendered);
            final double _tmpChange;
            _tmpChange = _cursor.getDouble(_cursorIndexOfChange);
            final String _tmpStatus;
            if (_cursor.isNull(_cursorIndexOfStatus)) {
              _tmpStatus = null;
            } else {
              _tmpStatus = _cursor.getString(_cursorIndexOfStatus);
            }
            _item = new Transaction(_tmpId,_tmpTransactionNumber,_tmpTimestamp,_tmpSubtotal,_tmpTax,_tmpTotal,_tmpPaymentType,_tmpTendered,_tmpChange,_tmpStatus);
            _result.add(_item);
          }
          return _result;
        } finally {
          _cursor.close();
        }
      }

      @Override
      protected void finalize() {
        _statement.release();
      }
    });
  }

  @Override
  public Object getTodaySales(final Continuation<? super Double> $completion) {
    final String _sql = "SELECT SUM(total) FROM transactions WHERE date(timestamp/1000, 'unixepoch') = date('now') AND status = 'COMPLETED'";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 0);
    final CancellationSignal _cancellationSignal = DBUtil.createCancellationSignal();
    return CoroutinesRoom.execute(__db, false, _cancellationSignal, new Callable<Double>() {
      @Override
      @Nullable
      public Double call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final Double _result;
          if (_cursor.moveToFirst()) {
            final Double _tmp;
            if (_cursor.isNull(0)) {
              _tmp = null;
            } else {
              _tmp = _cursor.getDouble(0);
            }
            _result = _tmp;
          } else {
            _result = null;
          }
          return _result;
        } finally {
          _cursor.close();
          _statement.release();
        }
      }
    }, $completion);
  }

  @NonNull
  public static List<Class<?>> getRequiredConverters() {
    return Collections.emptyList();
  }
}
