package com.ps.pos.data.dao;

import android.database.Cursor;
import androidx.annotation.NonNull;
import androidx.room.CoroutinesRoom;
import androidx.room.EntityDeletionOrUpdateAdapter;
import androidx.room.EntityInsertionAdapter;
import androidx.room.RoomDatabase;
import androidx.room.RoomSQLiteQuery;
import androidx.room.util.CursorUtil;
import androidx.room.util.DBUtil;
import androidx.sqlite.db.SupportSQLiteStatement;
import com.ps.pos.data.entities.LineItem;
import java.lang.Class;
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
public final class LineItemDao_Impl implements LineItemDao {
  private final RoomDatabase __db;

  private final EntityInsertionAdapter<LineItem> __insertionAdapterOfLineItem;

  private final EntityDeletionOrUpdateAdapter<LineItem> __deletionAdapterOfLineItem;

  private final EntityDeletionOrUpdateAdapter<LineItem> __updateAdapterOfLineItem;

  public LineItemDao_Impl(@NonNull final RoomDatabase __db) {
    this.__db = __db;
    this.__insertionAdapterOfLineItem = new EntityInsertionAdapter<LineItem>(__db) {
      @Override
      @NonNull
      protected String createQuery() {
        return "INSERT OR REPLACE INTO `line_items` (`id`,`transactionId`,`productId`,`productName`,`quantity`,`unitPrice`,`totalPrice`,`isVoided`) VALUES (nullif(?, 0),?,?,?,?,?,?,?)";
      }

      @Override
      protected void bind(@NonNull final SupportSQLiteStatement statement,
          @NonNull final LineItem entity) {
        statement.bindLong(1, entity.getId());
        if (entity.getTransactionId() == null) {
          statement.bindNull(2);
        } else {
          statement.bindLong(2, entity.getTransactionId());
        }
        statement.bindLong(3, entity.getProductId());
        if (entity.getProductName() == null) {
          statement.bindNull(4);
        } else {
          statement.bindString(4, entity.getProductName());
        }
        statement.bindDouble(5, entity.getQuantity());
        statement.bindDouble(6, entity.getUnitPrice());
        statement.bindDouble(7, entity.getTotalPrice());
        final int _tmp = entity.isVoided() ? 1 : 0;
        statement.bindLong(8, _tmp);
      }
    };
    this.__deletionAdapterOfLineItem = new EntityDeletionOrUpdateAdapter<LineItem>(__db) {
      @Override
      @NonNull
      protected String createQuery() {
        return "DELETE FROM `line_items` WHERE `id` = ?";
      }

      @Override
      protected void bind(@NonNull final SupportSQLiteStatement statement,
          @NonNull final LineItem entity) {
        statement.bindLong(1, entity.getId());
      }
    };
    this.__updateAdapterOfLineItem = new EntityDeletionOrUpdateAdapter<LineItem>(__db) {
      @Override
      @NonNull
      protected String createQuery() {
        return "UPDATE OR ABORT `line_items` SET `id` = ?,`transactionId` = ?,`productId` = ?,`productName` = ?,`quantity` = ?,`unitPrice` = ?,`totalPrice` = ?,`isVoided` = ? WHERE `id` = ?";
      }

      @Override
      protected void bind(@NonNull final SupportSQLiteStatement statement,
          @NonNull final LineItem entity) {
        statement.bindLong(1, entity.getId());
        if (entity.getTransactionId() == null) {
          statement.bindNull(2);
        } else {
          statement.bindLong(2, entity.getTransactionId());
        }
        statement.bindLong(3, entity.getProductId());
        if (entity.getProductName() == null) {
          statement.bindNull(4);
        } else {
          statement.bindString(4, entity.getProductName());
        }
        statement.bindDouble(5, entity.getQuantity());
        statement.bindDouble(6, entity.getUnitPrice());
        statement.bindDouble(7, entity.getTotalPrice());
        final int _tmp = entity.isVoided() ? 1 : 0;
        statement.bindLong(8, _tmp);
        statement.bindLong(9, entity.getId());
      }
    };
  }

  @Override
  public Object insert(final LineItem lineItem, final Continuation<? super Unit> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Unit>() {
      @Override
      @NonNull
      public Unit call() throws Exception {
        __db.beginTransaction();
        try {
          __insertionAdapterOfLineItem.insert(lineItem);
          __db.setTransactionSuccessful();
          return Unit.INSTANCE;
        } finally {
          __db.endTransaction();
        }
      }
    }, $completion);
  }

  @Override
  public Object insertAll(final List<LineItem> lineItems,
      final Continuation<? super Unit> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Unit>() {
      @Override
      @NonNull
      public Unit call() throws Exception {
        __db.beginTransaction();
        try {
          __insertionAdapterOfLineItem.insert(lineItems);
          __db.setTransactionSuccessful();
          return Unit.INSTANCE;
        } finally {
          __db.endTransaction();
        }
      }
    }, $completion);
  }

  @Override
  public Object delete(final LineItem lineItem, final Continuation<? super Unit> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Unit>() {
      @Override
      @NonNull
      public Unit call() throws Exception {
        __db.beginTransaction();
        try {
          __deletionAdapterOfLineItem.handle(lineItem);
          __db.setTransactionSuccessful();
          return Unit.INSTANCE;
        } finally {
          __db.endTransaction();
        }
      }
    }, $completion);
  }

  @Override
  public Object update(final LineItem lineItem, final Continuation<? super Unit> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Unit>() {
      @Override
      @NonNull
      public Unit call() throws Exception {
        __db.beginTransaction();
        try {
          __updateAdapterOfLineItem.handle(lineItem);
          __db.setTransactionSuccessful();
          return Unit.INSTANCE;
        } finally {
          __db.endTransaction();
        }
      }
    }, $completion);
  }

  @Override
  public Flow<List<LineItem>> getByTransactionId(final long transactionId) {
    final String _sql = "SELECT * FROM line_items WHERE transactionId = ?";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 1);
    int _argIndex = 1;
    _statement.bindLong(_argIndex, transactionId);
    return CoroutinesRoom.createFlow(__db, false, new String[] {"line_items"}, new Callable<List<LineItem>>() {
      @Override
      @NonNull
      public List<LineItem> call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfId = CursorUtil.getColumnIndexOrThrow(_cursor, "id");
          final int _cursorIndexOfTransactionId = CursorUtil.getColumnIndexOrThrow(_cursor, "transactionId");
          final int _cursorIndexOfProductId = CursorUtil.getColumnIndexOrThrow(_cursor, "productId");
          final int _cursorIndexOfProductName = CursorUtil.getColumnIndexOrThrow(_cursor, "productName");
          final int _cursorIndexOfQuantity = CursorUtil.getColumnIndexOrThrow(_cursor, "quantity");
          final int _cursorIndexOfUnitPrice = CursorUtil.getColumnIndexOrThrow(_cursor, "unitPrice");
          final int _cursorIndexOfTotalPrice = CursorUtil.getColumnIndexOrThrow(_cursor, "totalPrice");
          final int _cursorIndexOfIsVoided = CursorUtil.getColumnIndexOrThrow(_cursor, "isVoided");
          final List<LineItem> _result = new ArrayList<LineItem>(_cursor.getCount());
          while (_cursor.moveToNext()) {
            final LineItem _item;
            final long _tmpId;
            _tmpId = _cursor.getLong(_cursorIndexOfId);
            final Long _tmpTransactionId;
            if (_cursor.isNull(_cursorIndexOfTransactionId)) {
              _tmpTransactionId = null;
            } else {
              _tmpTransactionId = _cursor.getLong(_cursorIndexOfTransactionId);
            }
            final long _tmpProductId;
            _tmpProductId = _cursor.getLong(_cursorIndexOfProductId);
            final String _tmpProductName;
            if (_cursor.isNull(_cursorIndexOfProductName)) {
              _tmpProductName = null;
            } else {
              _tmpProductName = _cursor.getString(_cursorIndexOfProductName);
            }
            final double _tmpQuantity;
            _tmpQuantity = _cursor.getDouble(_cursorIndexOfQuantity);
            final double _tmpUnitPrice;
            _tmpUnitPrice = _cursor.getDouble(_cursorIndexOfUnitPrice);
            final double _tmpTotalPrice;
            _tmpTotalPrice = _cursor.getDouble(_cursorIndexOfTotalPrice);
            final boolean _tmpIsVoided;
            final int _tmp;
            _tmp = _cursor.getInt(_cursorIndexOfIsVoided);
            _tmpIsVoided = _tmp != 0;
            _item = new LineItem(_tmpId,_tmpTransactionId,_tmpProductId,_tmpProductName,_tmpQuantity,_tmpUnitPrice,_tmpTotalPrice,_tmpIsVoided);
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

  @NonNull
  public static List<Class<?>> getRequiredConverters() {
    return Collections.emptyList();
  }
}
